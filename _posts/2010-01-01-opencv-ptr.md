---
title: "OpenCV 源码中的安全指针和指针对齐"
category: coding
tags: [opencv, image]
---

# OpenCV 2.0

OpenCV 2.0中为很多1.0中 `C` 语言的数据结构提供了 `C++` 的类了，考虑到兼容性，保留旧的API。但是凭借C++构造和析造的功能，OpenCV2.0的内存管理方便了许多，使用新API的代码中类似 `cvRelease`的代码将不复存在。同时CV2.0也提供了一个安全指针类，让旧的需要手动管理内存的数据结构（如`IplImage`, `CvMat`等）也可以不用手动释放了，快哉！不过推荐直接用新的API(一些是仿Matlab的)，如`Mat`，程序可以更简洁、更直观。一个精典的OpenCV的Hello World程序现在可以这样写：

```cpp
#include <cv.h>
#include <highgui.h>

using namespace cv;

#ifdef _DEBUG
#pragma comment(lib, "cv200d.lib")
#pragma comment(lib, "cxcore200d.lib")
#pragma comment(lib, "highgui200d.lib")
#else
#pragma comment(lib, "cv200.lib")
#pragma comment(lib, "cxcore200.lib")
#pragma comment(lib, "highgui200.lib")
#endif // _DEBUG

const string WIN_NAME = "Lena";

int main(int argc, char* argv[])
{
    Mat img = imread("lena.jpg");
    namedWindow(WIN_NAME, CV_WINDOW_AUTOSIZE);
    imshow(WIN_NAME, img);
    waitKey(0);

    return 0;
}
```

# 安全指针
如果你还是习惯用CV1.0的API，那一定要试试CV2.0的安全指针（也叫智能指针）`Ptr` template。据说这个是参考了 [C++0x](http://en.wikipedia.org/wiki/C%2B%2B0x)和 [Boost](http://en.wikipedia.org/wiki/Boost_C%2B%2B_Libraries) 库的相关技术。使用也很简单：

```cpp
Ptr<IplImage> img = cvReadImage("lena.jpg"); // 不用cvReleaseImage();
```

我把 `Ptr` 类从 OpenCV 中独立出来，template class 定义如下：

```cpp
template<typename Tp> class Ptr
{
public:
    Ptr();
    Ptr(Tp* obj);
    ~Ptr();
    Ptr(const Ptr& ptr);
    Ptr& operator = (const Ptr& ptr);
    void addref(); 
    void release();
    void deleteobj();
    bool empty() const;

    Tp* operator -> ();
    const _Tp* operator -> () const;

    operator _Tp* ();
    operator const _Tp() const;
protected:
    _Tp obj;
    int* refcount;
};
```

简单地说，就是加了个指针引用数(refcount)和一些方便调用的操作符重装(`operator->()`)。值得注意的是，`Ptr` template 对指针指向的对象有一个要求，就是可以用`delete`操作土符来释放内存。你可能就想到`IplImage`就不满足这个要求了，这怎么办？可以使用模板特化（template specialization）重载 `Ptr<Iplimage>::delete_obj()` 函数：

```cpp
template<> inline void Ptr<IplImage>::deleteobj()
{
    cvReleaseImage(&obj);
}
```

PS：考虑到多线程时，CV2.0中的一些基本操作（如加法运算`CV_ADD`）都写成了函数或宏，保证互斥资源访问安全，看源代码时可注意下。

# 指针对齐

指针对齐也可以叫作内存地址对齐，主要是考虑到在一些架构上，只有被指定数（如`4`）整除的内存地址才可以正常访问，否则程序就会Crash了。CV2.0中的很多指针都是“对齐”过的，如指针的地址都是可以被`16`整除。CV2.0的内存主要是通过 `malloc`来分配的，返回的内存地址不可能都可以被`16`整除，所以要进行对齐操作。那如何对齐，对齐后截断后剩下来的内存怎么维护？

CV2.0的这样维护的：在`malloc`是多申请一个指针的空间，这个指针指向`malloc`得到的真实内存地址，只在`free`时使用它。相关函数有

```cpp
typedef unsigned char uchar;
#define CVMALLOCALIGN 16
//////////////////////////////////////////////////////////////////////////

template<typename Tp> static inline _Tp* alignPtr(Tp* ptr, int n=(int)sizeof(Tp))
{
    return (Tp)(((sizet)ptr + n-1) & -n);
}

_declspec(dllexport) void fastMalloc( sizet size )
{
    uchar* udata = (uchar)malloc(size + sizeof(void) + CVMALLOCALIGN); 
                                            // ^－ HERE 多申请一个 void* 的空间，
                                            //     用于存储 udata
    uchar** adata = alignPtr((uchar**)udata + 1, CVMALLOCALIGN);
    adata[-1] = udata; // <- 存储 udata
    return adata;
}

declspec(dllexport) void fastFree(void* ptr)
{
    if(ptr)
    {
        uchar* udata = ((uchar*)ptr)[-1];
        assert(udata < (uchar)ptr &&
            ((uchar*)ptr - udata) <= (ptrdifft)(sizeof(void*)+CVMALLOCALIGN)); 
        free(udata);
    }
}
```

# Reference

- OpenCV2.0 自带的《The Reference Manual)
- [What is "Pointer Alignment"](http://bytes.com/topic/c/answers/213142-what-pointer-alignment)
</ol>
