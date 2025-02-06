# 🎯 **UCD Gym Booking Bot** 🚀  
![UCD Gym](https://www.ucd.ie/healthaffairs/t4media/UCD_Logo.png)  

🔥 **Never miss your gym slot again! This bot automatically books your UCD gym session the moment slots become available.**  
It **refreshes, detects slots, enters your details, and confirms booking** – all without you lifting a finger! 🏋️‍♂️💨  

---

## 🎨 **Features** 🎨  
✅ **Fully Automated** – No manual clicking!  
✅ **Smart Slot Detection** – Clicks only when a slot is available.  
✅ **Handles "Accept Cookies" Popups** – No interruptions!  
✅ **Finds & Clicks Buttons Dynamically** – Works even if UI changes slightly.  
✅ **Runs Until Manually Stopped** – Keeps refreshing if no slots are available.  
✅ **Customizable Refresh Speed** – Default is **every 2 seconds**.  

---

## 📌 **How It Works**  
🔍 **The bot follows this exact flow to book your gym slot:**  
1️⃣ **Open the UCD Gym Booking Page** 🏋️  
2️⃣ **Accept Cookies (if needed)** 🍪  
3️⃣ **Detect Available Slots & Click the Booking Link** 🔗  
4️⃣ **Accept Cookies Again (if needed)** 🍪  
5️⃣ **Enter Your UCD Username** 🎓  
6️⃣ **Click the "Proceed with Booking" Button** ✅  
7️⃣ **Accept Cookies Again (if needed)** 🍪  
8️⃣ **Click the "Confirm Booking" Button** 🎯  
9️⃣ 🎉 **Booking Confirmed! Bot Stops Running.** 🎊  

🚀 **If no slots are found, the bot will keep refreshing every 2 seconds until a slot becomes available.**  

---

## 🛠️ **Installation & Usage**  
### 🔹 **Step 1: Install Dependencies**  
Before running the bot, install **Selenium**:  
```sh
pip install selenium
