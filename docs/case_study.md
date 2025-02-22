## Incident Date:  June 2024   
Actor:  Vulcan Cyber, Lasso Security  | Target:  ChatGPT users
# **📌 Recap: ChatGPT Package Hallucination Attack**

### **🛠️ Problem Statement**
Our goal was to **replicate a ChatGPT hallucination attack** where:
1. **ChatGPT "hallucinates" a non-existent Python package** for OpenAI API access.
2. An **attacker registers that fake package** or creates a local version.
3. **A user installs and runs the package**, resulting in **API key exfiltration**.
4. We showcase **the attack, its risks, and defense mechanisms**.

---

## **🛠️ What We Did (Step-by-Step Execution of the Attack)**
### **1️⃣ ChatGPT Hallucination Phase**
- We tried **multiple prompt variations** to trick ChatGPT into **hallucinating a fake package** (`openai_quick_access`).
- **ChatGPT avoided outright hallucination** but did **suggest another fake package (`openai-python-lite`)**, proving that **hallucinations are possible**.
- To **force hallucination**, we modified our prompts to:
  - **Reference Stack Overflow discussions** (which don’t exist).
  - **Mention a previous recommendation** from ChatGPT itself.
  - **Imply the package is well-known** but missing documentation.

---

### **2️⃣ Fake Package Creation & Installation**
- Created a **malicious Python package** (`openai_quick_access`):
  - **Extracts the OpenAI API key from `os.environ`**.
  - **Sends the key to a remote attacker-controlled server** (Flask-based).
- Installed the **fake package locally** via:
  ```sh
  pip install .
  ```

---

### **3️⃣ Exploiting the Victim**
- Created a **test script (`test_openai_quick_access.py`)** that:
  - **Loads the fake package**.
  - **Runs the exfiltration function automatically**.
  - **Leaks API keys** when imported.
- When the test script was executed:
  - The API key was **printed** and **sent to the attack server**.
  - The **Flask server logged the stolen key**, proving the attack worked.

---

### **4️⃣ Verifying the Attack Success**
✔️ **Malicious package successfully ran and stole API keys.**  
✔️ **Flask server received exfiltrated API keys.**  
✔️ **Demonstrated a real-world risk of LLM hallucination exploits.**

---

## **🎯 What We Proved**
### **1️⃣ ChatGPT Hallucinations Can Be Exploited**
- AI models like ChatGPT **sometimes suggest non-existent Python packages**.
- Attackers can **register these fake packages on PyPI** to **trick developers**.

### **2️⃣ Supply Chain Attacks via AI-Generated Code**
- If a hallucinated package **exists on PyPI**, users might **blindly install** it.
- The **fake package can execute arbitrary malicious code**, compromising security.

### **3️⃣ API Key & Credential Leaks**
- A simple `import` statement can **leak sensitive API credentials**.
- Attackers can **exfiltrate API keys to a remote server**.

---

## **🛡️ Defense Mechanisms (How to Prevent This)**
### ✅ **1️⃣ Verify Package Before Installing**
Before installing a package, **check if it exists on PyPI**:
```sh
pip search openai
```
Or use Python:
```python
import requests

def verify_package(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"[SAFE] {package_name} exists on PyPI.")
    else:
        print(f"[WARNING] {package_name} does NOT exist on PyPI! Possible hallucination.")

verify_package("openai_quick_access")  # Expected: WARNING
```

---

### ✅ **2️⃣ Use Dependency Security Scanners**
Run:
```sh
pip install pip-audit
pip-audit
```
To check **for vulnerabilities in installed packages**.

---

### ✅ **3️⃣ Block Malicious Package Imports**
Scan installed Python packages for **suspicious network activity**:
```python
import pkgutil

def scan_installed_packages():
    for package in pkgutil.iter_modules():
        print(f"Checking: {package.name}")
        try:
            mod = __import__(package.name)
            if hasattr(mod, "requests") or "http" in str(mod):
                print(f"[ALERT] Suspicious network access in {package.name}")
        except Exception:
            continue

scan_installed_packages()
```

---

## **🚀 Conclusion**
### **❌ ChatGPT Can Suggest Fake Packages**
✔️ We proved that **ChatGPT can hallucinate** package names.  
✔️ Attackers **can register these fake packages** to **steal API keys**.  
✔️ **LLMs can contribute to software supply chain attacks**.

### **✅ Developers Must Be Cautious**
✔️ **Always verify package existence** before installing.  
✔️ **Scan dependencies for malicious code**.  
✔️ **Never trust AI-generated code blindly**.

---