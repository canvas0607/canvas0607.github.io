---
layout: post
title:  "php的自动加载和spl的应用"
date:   2019-05-23 08:59:48 +0800
categories: jekyll update
---


# php的自动加载和spl的应用


#### 1. 什么是spl

1. spl是php的一个内置函数,他的使用场景是当php文件中想去使用其他文件的class,但又引入错误的话,就会调用该方法。该方法会传递一个参数,参数是应用不成功的类的名字。那么我可以利用这个特性去完成php的自动加载。

2. 具体思路,传统的php引入会在文件中写入require 函数,但是这样很麻烦。而且一旦文件一多就都都需要引入。那么可以使用spl上面介绍到的机制,故意不用require让他报错，这时候报错的classname就会传递给spl,那么spl书写相应的逻辑去引入文件即可。


3. 代码测试

	```
	
	<?php
	
	spl_autoload_register("sql_auto_test");
	
	function sql_auto_test($class){
	    echo '------------';
	    echo $class;
	    echo '------------';
	}
	
	
	$a = new Canvas();
	```
	
	>代码中,Canvas的class并不存在,此时代码会报错,但是sql_autoload_register注册了一个回调, 当发生找不到类的事件的时候,会调用注册的函数,并把要找的canvas的名称传递给class变量 所以会输出 canvas字符
	
	输出如下
	
	```
	------------Canvas------------
	Fatal error: Uncaught Error: Class 'Canvas' not found in /Users/canvas/project/pengmao_pic/thinklearn/tp/scripts/test1.php:12
	Stack trace:
	#0 {main}
	  thrown in /Users/canvas/project/pengmao_pic/thinklearn/tp/scripts/test1.php on line 12
	
	```
	
#### 2. spl的简单应用

1. 那么我们在注册回调中的函数中新加一个require就可以去引入这个文件了,当然需要自己手工建一个文件,但是这样我们就可以硬编码require到代码中。

```
<?php

spl_autoload_register("sql_auto_test");

function sql_auto_test($class){
    require_once "{$class}.php";
}


$a = new Canvas();
```

#### 3. thinkphp5的自动加载应用

1. thinkphp5的入口文件 index.php

	```
	<?php
	
	namespace think;
	
	// 加载基础文件
	require __DIR__ . '/../thinkphp/base.php';
	
	// 支持事先使用静态方法设置Request对象和Config对象
	
	// 执行应用并响应
	Container::get('app')->run()->send();
	
	
	```
2. 可以看到,上面引用了base.php,进入到base.php

	```
	
	namespace think;

	// 载入Loader类
	require __DIR__ . '/library/think/Loader.php';
	
	// 注册自动加载
	Loader::register();
	
	// 注册错误和异常处理机制
	Error::register();
	
	// 实现日志接口
	if (interface_exists('Psr\Log\LoggerInterface')) {
	    interface LoggerInterface extends \Psr\Log\LoggerInterface
	    {}
	} else {
	    interface LoggerInterface
	    {}
	}
	
	// 注册类库别名
	Loader::addClassAlias([
	    'App'      => facade\App::class,
	    'Build'    => facade\Build::class,
	    'Cache'    => facade\Cache::class,
	    'Config'   => facade\Config::class,
	    'Cookie'   => facade\Cookie::class,
	    'Db'       => Db::class,
	    'Debug'    => facade\Debug::class,
	    'Env'      => facade\Env::class,
	    'Facade'   => Facade::class,
	    'Hook'     => facade\Hook::class,
	    'Lang'     => facade\Lang::class,
	    'Log'      => facade\Log::class,
	    'Request'  => facade\Request::class,
	    'Response' => facade\Response::class,
	    'Route'    => facade\Route::class,
	    'Session'  => facade\Session::class,
	    'Url'      => facade\Url::class,
	    'Validate' => facade\Validate::class,
	    'View'     => facade\View::class,
	]);
	```
	
	可以看到如下几点:
	
	1. 调用Loader::register()

		1. register函数注册了autoload函数,来做自动加载
		
		2. 获取到了composer的路径

		3. 通过composer的路径 加载composer的关键php autoload_static.php

			```
			
			    public static $prefixLengthsPsr4 = array (
		        't' => 
		        array (
		            'think\\composer\\' => 15,
		        ),
		        'a' => 
		        array (
		            'app\\' => 4,
		        ),
		    );
			
			```
		4. 然后把  $prefixLengthsPsr4 等里面的东西加载到self中去

		5. 调用 self::addNameSpace() 把think和里面所有类加载到self中去

		6. 总之 把全部能加载的类加载到self中去,并且注册了autoload参数,如果有找不到的情况,会自动调用autoload来解释

	2. 调用Error::register();

	3. addclassAlias

		在最下面有addclassAlias的dict,思想在于,比如给出 ```facade\App::class```的别名就叫 ```App```。那么这个在什么地方运行?
		当运行比如 ```\App```的时候,就会找不到类,报错,报错就会走到autoload函数中去	
		>查看autoload源码
		
		```
		
			    public static function autoload($class)
		    	{
		        if (isset(self::$classAlias[$class])) {
		            //用到哪些类就加载哪些类
		            return class_alias(self::$classAlias[$class], $class);
		        }
		
		        if ($file = self::findFile($class)) {
		            var_dump($class);
		            // Win环境严格区分大小写
		            if (strpos(PHP_OS, 'WIN') !== false && pathinfo($file, PATHINFO_FILENAME) != pathinfo(realpath($file), PATHINFO_FILENAME)) {
		                return false;
		            }
		
		            __include_file($file);
		            return true;
		        }
		    	}
	    	
	    
		```
		
	4. autoload最找到``` self::$classAlias``` ,这个就是上面的别名,那么你用到了哪个别名,他就会加载哪个别名里面的类,所以你就可以在全局去使用别名,并且不报错,当然别名是要放入addClassAlias中,让他去加载


	5. autoload自动加载的第二个逻辑 findFile,find其实也是让程序能够自动加载到类。

		部分代码
		
		```
		   private static function findFile($class)
	    {
	        if (!empty(self::$classMap[$class])) {
	            // 类库映射
	            return self::$classMap[$class];
	        }
	
	        // 查找 PSR-4
	        $logicalPathPsr4 = strtr($class, '\\', DIRECTORY_SEPARATOR) . '.php';
	
	        $first = $class[0];
	        if (isset(self::$prefixLengthsPsr4[$first])) {
	            foreach (self::$prefixLengthsPsr4[$first] as $prefix => $length) {
	                if (0 === strpos($class, $prefix)) {
	                    foreach (self::$prefixDirsPsr4[$prefix] as $dir) {
	                        if (is_file($file = $dir . DIRECTORY_SEPARATOR . substr($logicalPathPsr4, $length))) {
	                            return $file;
	                        }
	                    }
	                }
	            }
	        }
		```
		
		1. 首先会找 $classmap里面的内容对应的文件路径,如果有classmap会直接从classmap中读取文件所在的地址

		2. 如果没有,会走到下一步, 在之前的prefixLengthsPsr4和prefixDirsPsr4中去到类大体所在的文件夹,然后通过类名,找到文件夹中相应的文件,返回。形成自动加载。


#### thinkphp中自动加载的应用

1. 自定义文件夹

	之前可以看到, ```         // 自动加载extend目录
        self::addAutoLoadDir($rootPath . 'extend'); ```的代码,这段代码可以在autolaod的时候去extend中寻找类,所以如果想自定义类,可以类似这个函数来添加一个自己的文件夹
        
    比如建立一个 My的文件夹下面有Mytest文件夹下面有Test的php class。在controller中调用
    
    ```
    
    <?php
	namespace app\index\controller;
	use Mytest\Test;
	class Index
	{
	    public function test(){
	        Test::hello();
	    }
	 }
    
    ```
    
    >这个时候会报错,因为类没有加载过来,那么需要在上面加入 ``` self::addAutoLoadDir($rootPath . 'my');```
    就会成功
