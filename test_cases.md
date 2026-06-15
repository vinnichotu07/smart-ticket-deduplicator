# 🧪 Test Cases - Smart Ticket Deduplicator

---

## ✅ Test Case 1: Login Issues

**Input:**
- "Login failure with 403 error"
- "Unable to login, access denied"

**Expected Output:**
✔ Same cluster (High similarity > 0.65)

---

## ✅ Test Case 2: Payment Problems

**Input:**
- "Payment failed during checkout"
- "Transaction error in payment gateway"

**Expected Output:**
✔ Same cluster (High similarity > 0.65)

---

## ⚠️ Test Case 3: UI Issue

**Input:**
- "Signup button not clickable"
- "Login page not loading"

**Expected Output:**
⚠ Different clusters (Low similarity)

---

## ⚠️ Test Case 4: Mixed Issues

**Input:**
- "Database timeout during checkout"
- "Payment failed at final step"

**Expected Output:**
⚠ Potential match (Medium similarity 0.45–0.65)

---

## ❌ Test Case 5: Completely Different Issues

**Input:**
- "Forgot password email not received"
- "App crashes when opening dashboard"

**Expected Output:**
❌ Not duplicate (<0.45 similarity)