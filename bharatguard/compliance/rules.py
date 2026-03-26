import re
from typing import List, Dict, Any, Callable

class ComplianceRule:
    def __init__(self, rule_id: str, category: str, description: str, severity: str, check_fn: Callable[[str], bool], fix_suggestion: str):
        self.rule_id = rule_id
        self.category = category
        self.description = description
        self.severity = severity
        self.check_fn = check_fn
        self.fix_suggestion = fix_suggestion

def check_regex(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, re.IGNORECASE))

# --- GST Rules ---
GST_RULES = [
    ComplianceRule("GST-001", "GST", "Ensure GSTIN validation logic is present", "high", 
                   lambda x: check_regex(r"gstin|tax_id|registration_number", x), 
                   "Add a validation function for 15-digit GSTIN (e.g., ^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$)"),
    ComplianceRule("GST-002", "GST", "HSN/SAC code field required for items", "medium",
                   lambda x: check_regex(r"hsn_code|sac_code", x),
                   "Include HSN (Harmonized System of Nomenclature) code for goods or SAC code for services in items."),
    ComplianceRule("GST-003", "GST", "Separate CGST, SGST, IGST calculation", "high",
                   lambda x: check_regex(r"cgst.*sgst|igst", x),
                   "Implement logic to split taxes into CGST/SGST (intra-state) or IGST (inter-state)."),
    ComplianceRule("GST-004", "GST", "Support for GST Rate slabs (5, 12, 18, 28)", "medium",
                   lambda x: check_regex(r"5|12|18|28", x),
                   "Ensure the tax calculation logic references the standard GST rate slabs."),
    ComplianceRule("GST-005", "GST", "Place of Supply detection", "medium",
                   lambda x: check_regex(r"place_of_supply|state_code", x),
                   "Add logic to determine the 'Place of Supply' to apply the correct GST type.")
]

# --- UPI Rules ---
UPI_RULES = [
    ComplianceRule("UPI-001", "UPI", "Standard VPA (Virtual Payment Address) format validation", "high",
                   lambda x: check_regex(r"vpa|upi_id", x),
                   "Add regex to validate UPI IDs (e.g., ^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}$)"),
    ComplianceRule("UPI-002", "UPI", "Transaction Limit enforcement", "medium",
                   lambda x: check_regex(r"limit|max_amount", x),
                   "Implement client-side or server-side checks for UPI transaction limits (e.g., 1 Lakh for P2P)."),
    ComplianceRule("UPI-003", "UPI", "Merchant Category Code (MCC) requirement", "medium",
                   lambda x: check_regex(r"mcc|merchant_category", x),
                   "Ensure MCC is passed in payment intents for merchant transactions."),
    ComplianceRule("UPI-004", "UPI", "Support for Dynamic QR Code generation", "medium",
                   lambda x: check_regex(r"qr_code|generate_qr", x),
                   "Implement UPI Deep-linking or QR generation following NPCI specifications (upi://pay?...)"),
    ComplianceRule("UPI-005", "UPI", "Intent flow vs Collect flow handling", "high",
                   lambda x: check_regex(r"intent|collect", x),
                   "Explicitly handle both intent (app-to-app) and collect (VPA-based) payment flows.")
]

# --- Aadhaar Rules ---
AADHAAR_RULES = [
    ComplianceRule("AAD-001", "Aadhaar", "Masked Aadhaar display", "high",
                   lambda x: check_regex(r"mask|last_4", x),
                   "Ensure Aadhaar numbers are never stored/displayed in full. Mask the first 8 digits."),
    ComplianceRule("AAD-002", "Aadhaar", "Purpose of Collection consent", "high",
                   lambda x: check_regex(r"consent|purpose", x),
                   "Explicitly collect and log the 'Purpose of Aadhaar Collection' as per UIDAI guidelines."),
    ComplianceRule("AAD-003", "Aadhaar", "Virtual ID (VID) preference", "medium",
                   lambda x: check_regex(r"vid|virtual_id", x),
                   "Prioritize using 16-digit Virtual ID over the 12-digit Aadhaar number."),
    ComplianceRule("AAD-004", "Aadhaar", "Redaction in documents", "medium",
                   lambda x: check_regex(r"redact|blur", x),
                   "If Aadhaar cards are uploaded, implement logic to automatically redact the full number in images."),
    ComplianceRule("AAD-005", "Aadhaar", "Strict Authentication Logging", "medium",
                   lambda x: check_regex(r"auth_log|uidai_response", x),
                   "Maintain detailed logs of authentication attempts without storing sensitive data.")
]

# --- DPDP Rules ---
DPDP_RULES = [
    ComplianceRule("DPD-001", "DPDP", "Notice for Data Collection", "high",
                   lambda x: check_regex(r"privacy_notice|data_usage", x),
                   "Provide a clear notice to the Data Principal at the time of collection."),
    ComplianceRule("DPD-002", "DPDP", "Consent Withdrawal mechanism", "high",
                   lambda x: check_regex(r"withdraw|opt_out", x),
                   "Implement a feature for users to easily withdraw their personal data consent."),
    ComplianceRule("DPD-003", "DPDP", "Data Localization check", "medium",
                   lambda x: check_regex(r"india_region|storage_location", x),
                   "Ensure critical personal data is stored within the territory of India."),
    ComplianceRule("DPD-004", "DPDP", "Right to Correction/Erasure", "medium",
                   lambda x: check_regex(r"delete_account|update_profile", x),
                   "Allow users to correct or delete their personal data."),
    ComplianceRule("DPD-005", "DPDP", "Data Fiduciary identification", "medium",
                   lambda x: check_regex(r"fiduciary", x),
                   "Identify the Data Fiduciary in terms of service and notices.")
]

# --- RBI/Security Rules ---
RBI_RULES = [
    ComplianceRule("RBI-001", "RBI", "End-to-End Encryption (AES-256)", "high",
                   lambda x: check_regex(r"aes|encrypt|cryptography", x),
                   "Use AES-256 for storing sensitive payment information."),
    ComplianceRule("RBI-002", "RBI", "Audit logging for sensitive actions", "medium",
                   lambda x: check_regex(r"audit_log|action_history", x),
                   "Maintain a timestamped audit trail for all sensitive financial operations."),
    ComplianceRule("RBI-003", "RBI", "Card Tokenization (instead of storing raw PAN)", "high",
                   lambda x: check_regex(r"token|vault", x),
                   "Do not store raw card numbers. Use network-level or issuer-level tokenization."),
    ComplianceRule("RBI-004", "RBI", "Session timeout (Auto-logout)", "medium",
                   lambda x: check_regex(r"timeout|session_expiry", x),
                   "Implement automatic session termination after a period of inactivity."),
    ComplianceRule("RBI-005", "RBI", "Two-Factor Authentication (2FA) enforcement", "high",
                   lambda x: check_regex(r"2fa|mfa|otp", x),
                   "Enforce 2FA/AFA (Additional Factor Authentication) for all financial transactions.")
]

ALL_RULES = GST_RULES + UPI_RULES + AADHAAR_RULES + DPDP_RULES + RBI_RULES
