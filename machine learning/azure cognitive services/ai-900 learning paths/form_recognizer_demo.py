# pip install azure_ai_formrecognizer
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
import matplotlib.pyplot as plt
from PIL import Image
import os

# Create a client for the form recognizer service
form_key = "KEY"
form_endpoint = "ENDPOINT"
form_recognizer_client = FormRecognizerClient(
    endpoint=form_endpoint,
    credential=AzureKeyCredential(form_key)
)

# Load and display a receipt image
fig = plt.figure(figsize=(6, 6))
image_path = os.path.join("resources", "receipt.jpg")

try:
    print("Analyzing receipt...")

    # Submit the file data to form recognizer
    with open(image_path, "rb") as f:
        analyze_receipt = form_recognizer_client.begin_recognize_receipts(
            receipt=f)

    # Get the results
    receipt_data = analyze_receipt.result()

    # Get the first (and only) receipt
    receipt = receipt_data[0]

    receipt_type = receipt.fields.get("ReceiptType")
    if receipt_type:
        print(F"Receipt Type: {receipt_type.value}")
    
    merchant_address = receipt.fields.get("MerchantAddress")
    if merchant_address:
        print(f"Merchant Address: {merchant_address.value}")
    
    merchant_phone = receipt.fields.get("MerchantPhoneNumber")
    if merchant_phone:
        print(f"Merchant Phone: {merchant_phone.value}")
    
    transaction_date = receipt.fields.get("TransactionDate")
    if transaction_date:
        print(f"Transaction Date: {transaction_date.value}")

    print("Receipt items:")    
    items = receipt.fields.get("Items")
    if items:
        for idx, item in enumerate(receipt.fields.get("Items").value):
            print(f"\tItem #{idx+1}")
            
            item_name = item.value.get("Name")
            if item_name:
                print(f"\t - Name: {item_name.value}")
            
            item_total_price = item.value.get("TotalPrice")
            if item_total_price:
                print(f"\t - Price: {item_total_price.value}")
    
    subtotal = receipt.fields.get("Subtotal")
    if subtotal:
        print(f"Subtotal: {subtotal.value}")
    
    tax = receipt.fields.get("Tax")
    if tax:
        print(f"Tax: {tax.value}")

    total = receipt.fields.get("Total")
    if total:
        print(f"Total: {total.value}")

except Exception as ex:
    print(f"Error: {ex}")
