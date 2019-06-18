---
layout: default
title: design pattern factory method(设计模式 工厂方法模式)
---
{{ page.title }}

1.假如你有一个比萨店,代码最初设计可能是这样的,
用户通过选择类型获取相应的 披萨。

GetPizza.php
```php
<?php
include_once 'CheeseTestPizza.php';
include_once 'GreekTestPizza.php';
include_once 'PizzaTestStore.php';

class PizzaTestStore
{
    private $pizza;
    public function orderPizza($type)
    {
        if($type == 'cheese'){
            $this->pizza = new CheeseTestPizza();
        }elseif ($type == 'greek'){
            $this->pizza = new GreekTestPizza();
        }elseif ($type == 'pepperoni'){
            $this->pizza = new PepperoniTestPizza();
        }
        $this->pizza->prepare();
        $this->pizza->bake();
        $this->pizza->cut();
        $this->pizza->box();

    }
}
```
CheeseTestPizza.php
```php
<?php
class CheeseTestPizza
{
    public function prepare(){
        echo "get cheese pizza! preparing\n";
    }

    public function bake(){
        echo  "bake the cheese pizza!\n";
    }

    public function cut(){
        echo "damn, i cut my hand\n";
    }

    public function box(){
        echo "boxing\n";
    }
}

```

2.但是这样如果新添加披萨会很麻烦,每增加(或者减少)一个披萨就必须修改,
就必须修改 PizzaTestStore.php 的代码。在这种情况下想到提取会变化的部分。
----------实现简单工厂。

PizzaTestStore.php
```php
<?php
include_once 'SimplePizzaTestFactory.php';
class PizzaTestStore
{
    private $pizza;
    private $factory;
    public function __construct()
    {
        $this->factory = new SimplePizzaTestFactory();
    }

    public function orderPizza($type)
    {
        $this->pizza = $this->factory->createPizza($type);

        $this->pizza->prepare();
        $this->pizza->bake();
        $this->pizza->cut();
        $this->pizza->box();

    }
}
```

SimplePizzaTestFactory.php
```php
<?php
include_once 'CheeseTestPizza.php';
include_once 'GreekTestPizza.php';
include_once 'PizzaTestStore.php';

class SimplePizzaTestFactory
{
    private $pizza;
    public function createPizza($type)
    {
        if($type == 'cheese'){
            $this->pizza = new CheeseTestPizza();
        }elseif ($type == 'greek'){
            $this->pizza = new GreekTestPizza();
        }elseif ($type == 'pepperoni'){
            $this->pizza = new PepperoniTestPizza();
        }
        return $this->pizza;
    }
}
```
现在增加或者减少披萨的逻辑就在SimplePizzaTestFactory里面实现,
不用更改 PizzaTestStore.php代码。

3.但是不是的地区同一种比萨的风味不同,比如有纽约,加州,芝加哥三个地区加盟,
他们都有各自的工厂,但是需要统一化管理,只是prepare，bake的方式各有不同。

PizzaTestStore.php
```php
<?php
class PizzaTestStore
{
    private $pizza;
    private $factory;
    public function __construct($factory)
    {
        $this->factory = $factory;
    }
    public function orderPizza($type)
    {
        $this->pizza = $this->factory->createPizza($type);

        $this->pizza->prepare();
        $this->pizza->bake();
        $this->pizza->cut();
        $this->pizza->box();

    }
}

```

NyPizzaTestFactory.php
```php
<?php
include_once 'CheeseTestPizza.php';
include_once 'GreekTestPizza.php';
include_once 'PepperoniTestPizza.php';
class NyPizzaTestFactory
{
    private $pizza;
    public function createPizza($type){
        if($type == 'cheese'){
            $this->pizza = new CheeseTestPizza();
        }elseif ($type == 'greek'){
            $this->pizza = new GreekTestPizza();
        }elseif ($type == 'pepperoni'){
            $this->pizza = new PepperoniTestPizza();
        }
        return $this->pizza;
    }
}
```

clientTest.php
```php
<?php
include_once 'PizzaTestStore.php';
include_once 'NyPizzaTestFactory.php';

$nyFactory = new NyPizzaTestFactory();
$test = new PizzaTestStore($nyFactory);
$test->orderPizza('cheese');

```

这样通过实例化不同的工厂,再将比萨交由客户

4.但是每次获得pizza都要依赖于PizzaTestStore,这样缺乏了弹性,从orderPizza方法来看,
它不要指导是哪个子类创建了pizza,他只要得到披萨,需要将创建pizza的方法交由子类决定。

PizzaTestStore.php
```php
<?php
abstract class PizzaTestStore
{
    private $pizza;

    public function orderPizza($type)
    {
        $this->pizza = $this->createPizza($type);

        $this->pizza->prepare();
        $this->pizza->bake();
        $this->pizza->cut();
        $this->pizza->box();
    }

    abstract function createPizza($type);
}

```

NyPizzaStore.php
```php
<?php
include_once 'CheeseTestPizza.php';
include_once 'GreekTestPizza.php';
include_once 'PepperoniTestPizza.php';
class NyPizzaStore extends PizzaTestStore
{
    private $pizza;

    public function createPizza($type){

        if($type == 'cheese'){
            $this->pizza = new CheeseTestPizza();
        }elseif ($type == 'greek'){
            $this->pizza = new GreekTestPizza();
        }elseif ($type == 'pepperoni'){
            $this->pizza = new PepperoniTestPizza();
        }
        return $this->pizza;

    }
}
```

clientTest.php
```php
<?php
include_once 'PizzaTestStore.php';
include_once 'NyPizzaStore.php';
$test = new NyPizzaStore();
$test->orderPizza('cheese');
```











