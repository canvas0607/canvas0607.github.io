# malloc 内存分配

#### 1. malloc的作用和原理

1. 栈区（stack）—由编译器自动分配释放，存放函数的参数值，局部变量的值等。其操作方式类似于数据结构中的栈。
2. 堆区（heap）—一般由程序员分配释放，若程序员不释放，程序结束时可能由OS回收。注意它与数据结构中的堆是两回事，分配方式倒是类似于链表。
3. 全局区（静态区）（static）—全局变量和静态变量的存储是放在一块的，初始化的全局变量和静态变量在一块区域，未初始化的全局变量和未初始化的静态变量在相邻的另一块区域。程序结束后由系统释放。
4. 文字常量区—常量字符串就是放在这里的。程序结束后由系统释放。
5. 程序代码区—存放函数体的二进制代码。


2. stack heap, malloc是程序分配后存储的位置在heap(堆)中

	```
	 int a=0;  //全局初始化区
	 char *p1;  //全局未初始化区
	 main()
	 {
	  intb;栈
	  char s[]="abc";  //栈
	  char *p2;     //栈
	  char *p3="123456";  //123456\0在常量区，p3在栈上。
	  static int c=0；  //全局（静态）初始化区
	  p1 = (char*)malloc(10);
	  p2 = (char*)malloc(20);  //分配得来得10和20字节的区域就在堆区。
	  strcpy(p1,"123456");  //123456\0放在常量区，编译器可能会将它与p3所向"123456"优化成一个地方。
	}
	
	```
	
#### 2. malloc的声明和分配方式和内存的变化

1. 必须因为头文件stdlib

	```
	#include <stdlib.h>
	```
	
2. 函数写法

	```
	#include <stdlib.h>
	int main(void){
	    //! showMemory(start=272)
	    malloc(5);
	    malloc(1);
	    return 0;
	}
	
	```
	
3. 具体分配图

	1. malloc是以4byte为单位进行分配的,所以填5会分配8byte空间
	
	2. 在分配时候左右两边会有4byte的空间,指明分配的信息
	
	3. 具体分配图
	
	<image src="pics/11_1.png">
	
	<br>
	
	<image src="pics/11_2.png">


#### 3.  使用malloc的空间

1. 代码

	```
	
	#include <stdlib.h>
	int main(void){
	    //! showMemory(start=272)
	    int * intptr;
	    double * doubleptr;
	    intptr = (int *) malloc(sizeof(int));
	    * intptr = 5;
	    doubleptr = (double *) malloc(sizeof(double));
	    * doubleptr = 9.0;
	    return 0;
	}
	```
	
2. 空间的分配

		
	<image src="pics/11_1.png">
	
	<br>
	
	<image src="pics/11_2.png">

3. 可以看到malloc分配的空间在低位内存,从下至上分配(heap),指针和变量空间在高位内存从上之下分配(stack)

#### 4. 强制类型转换

1. 如下代码

	```
	
	intptr = (int *) malloc(sizeof(int));
	* intptr = 5;
	doubleptr = (double *) malloc(sizeof(double));
	* doubleptr = 9.0;
	```
	
2. 解释

	malloc返回的是 void *,如果上面声明了 int * ,那么需要强制转换为 int * 类型来接受malloc
	
3. 如果改成 char会有什么影响?

	

	```
	#include <stdlib.h>
	int main(void){
	    //! showMemory(start=272)
	    char * intptr;
	    double * doubleptr;
	    intptr = (char *) malloc(8);
	    * intptr = 5;
	    * (intptr + 1) = 1;
	    doubleptr = (double *) malloc(sizeof(double));
	    * doubleptr = 9.0;
	    return 0;
	}
	```
	
	>我们把intprt改为了char *类型,那么指针的下一个值就会指向下<strong>1个<strong>的地址空间，5就会附在下一个地址空间
	
	如图
	
	<image src="pics/11_5.png">
	
#### <a href="blog12_c_pointer.md">void * , int * ,  char * ,不同点 <a>



