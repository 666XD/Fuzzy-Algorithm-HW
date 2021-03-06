# Fuzzy Algorithm apply on self-driving car

## 介紹

### 程式使用說明簡介

此程式是用 **python3.6** 來撰寫的，
需求的 package 如下:
```python=3.6
import sys, pygame
import os
import time
import math
```
主程式為 `autoCar.py`

* **執行檔**-的部分，請到 `FuzzyExe\autoCar.exe` 點擊執行
* **地圖地圖切換**-的部分，請將任何要執行的地圖請命名為 `FuzzyExe\map.txt`
* **Log**-的輸出位子位於 `FuzzyExe\log`內
* **去模糊化** 我用寫了三種不同的去模糊化方法分別如下:
    1. Functional base fuzzy
    2. Center Gravity fuzzy
    3. Mean Max fuzzy

    欲更改程式模糊化的方法，請到`FuzzyExe\Mthod.txt`文件內，將下列不同方法名稱覆蓋貼上儲存即可，名稱方法分別為:
    1. Fuzzy
    2. FuzzyGravity
    3. FuzzyMean

本執行檔已在乾淨的 window7 模擬器下執行通過
:::danger
:fire: 
1. 注意! 在模擬機內如果不能順利執行的話，可能是缺少 visual studio 某些套件，文件中附帶了兩個安裝檔，分別是(32/64)位元的vc_redist.x64，請依照系統擇一安裝後即可成功執行。 
2. 請勿單獨拷貝EXE到虛擬機內，程式執行需要整個檔案夾的資料。
3. 執行的檔案夾路徑不可有中文，例如 功課\執行檔\ ... ，要改成 homeWork\EXE\... ，不然會失敗執行。 因此我的上交的檔名沒有中文。
:::

## 說明與設計

### 程式碼說明
程式碼分成三大部分，分別為圖像的顯示、車子的移動與距離角度監測、最後是Fuzzy的運算
* 動畫遊戲的產生我是用pygame來進行製作，分別是程式391行以後
* 車子的移動和距離監測分別由程式的 201~391 行開始，對於車子的的距離，我先去判斷車子在固定角度射出的線是否與地圖邊界相交，再判別兩線之間是交於哪一點，因而算出車子前中右不同方位對地圖邊界的距離。而車子的移動是由課本提供的公式來對角度做運算，公式如下:
![](https://i.imgur.com/pzYNkQS.png)
* Fuzzy 的運算於程式的 0~201，其中包含了三種不同去模糊化的方法與系統輸出入的參數設定，詳細解說請看模糊規則設計。
而對於程式本身，我會對於左中右的距離先去找出他們交於感測函數的那些點，拿這些點與輸出角度函數做運算，運算內容會因去模糊化方法不同而有所差異。

程式內有對每個 function 做詳細註解

### 模糊規則設計

模糊規則如下

* 此為對於距離感測的函數設計
![](https://i.imgur.com/W5KCbX8.jpg)

* 此為對於距離對於輸出角度的函數設計
![](https://i.imgur.com/68LBdUp.jpg)

## 實驗結果

### 設定層面
對於汽車的左右兩側角度，若設角度為90^o^時，會造成汽車不穩定，找尋到正確方向的效果較差等問題，所以目前左右的夾角是設是設45^o^，在這情況下模型車運行的非常的穩定

### 去模糊化
去模糊化的這個部分，我分別做了函數加權、重心法、與最大平均法這三個方法

**函數加權**的移動路徑如下。 可以看到路徑在第一個夾角的部分多做了一個迴轉才轉入正常的路線
![](https://i.imgur.com/38ZrlX7.jpg)

而在**重心法**與**最大平均法**的部分，分別接穩定的朝終點邁進。但與最大平均法比較起來，重心法還是較為穩定，平均法則是在車頭的部分會快速左右晃動，而稍覺不穩定。
(以下圖片為重心法)
![](https://i.imgur.com/23jmbzF.jpg)

### 附錄

* 實驗結果的 LOG `train4D.txt` and `train6D.txt`，檔案放置位置於 `FuzzyExe/log` 目錄底下。
* 在程式執行結束後，會自動輸出帶有移動軌跡的執行截圖於工作目錄底下
* 若有需要實際Demo或是執行起來有問題，希望助教聯絡我: leo8387@gmail.com