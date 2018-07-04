---
layout: post
title: "ON_MESSAGE使用方法"
category: coding
tags: [mfc]
---

ON_MESSAGE 响应的是自定义消息,有关自定义消息的处理请看如下步骤:


# 定义消息

在CCDlg类的头文件中加入如下代码：

```cpp
#define WM_CUSTOMIZE WM_USER+1
```

头文件中加入Customize的声明：

```cpp
afx_msg LRESULT Customize(WPARAM wParam, LPARAM lParam);
```

# cpp文件中加入消息的注

```cpp
ON_MESSAGE(WM_CUSTOMIZE, Customize)
```



# 加入消息响应函数实现

在CCDlg类的实现文件中加入消息响应函数的实现部分，代码如下：

```cpp
void CCDlg::Customize(WPARAM wParam, LPARAM lParam) 
{ 
    CString strTittle; 
    strTittle.Format("自定义消息参数：x=%d,y=%d",wParam,lParam); 
    SetWindowText(strTittle); 
}
```

# 显式地发送消息

在主框架的 帮助 主菜单中加入 自定义消息 子菜单，其ID设为ID_CUSTOMIZE，通过类向导响应该命令，函数名默认。其函数体如下：

```cpp
void CMainFrame::OnCustomize() 
{ 
    POINT pos; 
    //将消息参数定义为屏幕坐标值 
    GetCursorPos(&pos); 
    pdlg->SendMessage(WM_CUSTOMIZE,(UINT)pos.x,pos.y); 
}
```

[原文](http://topic.csdn.net/u/20080702/15/b1118332-f27c-4b42-b97e-9a988bca9d96.html)
