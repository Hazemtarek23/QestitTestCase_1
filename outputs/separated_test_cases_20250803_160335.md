# Test Cases Report - Separated Steps & Data

**Total Test Cases:** 65
**Generated On:** 2025-08-03 16:03:35

## Test Case Summary by Category

- **Functional:** 18 test cases
- **Security:** 13 test cases
- **Boundary:** 5 test cases
- **Usability:** 7 test cases
- **Error Handling:** 7 test cases
- **Performance:** 8 test cases
- **Integration:** 7 test cases

---

## Test Case 1: Successful Corporate User Registration

**Test ID:** TC_001
**Module:** User Management > User Registration
**Category:** Functional
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 5 minutes

**Description:** Validate that a new corporate user can be registered with valid details and assigned to the correct role and group.

**Objective:** Ensure user registration works as expected and user is mapped to the correct role/group.

**Preconditions:**
- Admin user is logged in
- Corporate customer profile exists

### Test Steps (Actions Only):

**Step 1:** Navigate to user registration page
**Step 2:** Enter full name
**Step 3:** Enter email address
**Step 4:** Enter mobile number
**Step 5:** Select user role
**Step 6:** Assign user to group
**Step 7:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Ahmed Youssef |
| email | ahmed.youssef@company.com |
| mobile | 01012345678 |
| role | Initiator |
| group | Tax Payment Group |

**Overall Expected Result:** User account is created, user is assigned to the selected role and group, and a registration confirmation email is sent.

**Validation Criteria:**
- User appears in user list
- Assigned role and group are correct
- Confirmation email is received

**Dependencies:** Corporate customer profile setup

**Notes:** Covers basic registration flow for new users.

---

## Test Case 2: Registration Fails with Invalid Email Format

**Test ID:** TC_002
**Module:** User Management > User Registration
**Category:** Functional
**Priority:** High
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 3 minutes

**Description:** Ensure the system rejects registration attempts with an invalid email address format.

**Objective:** Verify email format validation works and error is displayed.

**Preconditions:**
- Admin user is logged in

### Test Steps (Actions Only):

**Step 1:** Navigate to user registration page
**Step 2:** Enter full name
**Step 3:** Enter invalid email address
**Step 4:** Enter mobile number
**Step 5:** Select user role
**Step 6:** Assign user to group
**Step 7:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Mona Khaled |
| email | mona.khaled@company |
| mobile | 01234567890 |
| role | Approver |
| group | Universal Collection Group |

**Overall Expected Result:** Registration is blocked, and a clear error message is displayed indicating invalid email format.

**Validation Criteria:**
- Error message is displayed
- User is not created

**Dependencies:** User registration page available

**Notes:** Tests input validation for email field.

---

## Test Case 3: Session Timeout After Inactivity

**Test ID:** TC_003
**Module:** Authentication > Session Management
**Category:** Security
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 20 minutes

**Description:** Check that user session is terminated after the configured period of inactivity.

**Objective:** Ensure session timeout is enforced for security.

**Preconditions:**
- User is logged in
- Session timeout is set to 15 minutes

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Remain inactive for the session timeout period
**Step 3:** Attempt to perform any action
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corporate.user@company.com |
| password | StrongPass!2024 |
| timeout | 15 minutes |

**Overall Expected Result:** User is logged out automatically after 15 minutes of inactivity and prompted to log in again.

**Validation Criteria:**
- Session expires after inactivity
- User is redirected to login page

**Dependencies:** Session timeout configuration

**Notes:** Validates session management and security compliance.

---

## Test Case 4: 2FA Required on Login

**Test ID:** TC_004
**Module:** Authentication > Login
**Category:** Security
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 4 minutes

**Description:** Ensure that users are required to complete two-factor authentication during login.

**Objective:** Verify 2FA is enforced and login is blocked without successful 2FA.

**Preconditions:**
- User account with 2FA enabled exists

### Test Steps (Actions Only):

**Step 1:** Navigate to login page
**Step 2:** Enter username
**Step 3:** Enter password
**Step 4:** Click login button
**Step 5:** Enter 2FA code
**Step 6:** Submit 2FA code
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | fatma.ali@company.com |
| password | SecurePass2024! |
| 2fa_code | 123456 |

**Overall Expected Result:** User is granted access only after successful 2FA; login is blocked if 2FA fails.

**Validation Criteria:**
- 2FA prompt appears after password entry
- Access is denied if 2FA is incorrect

**Dependencies:** 2FA system operational

**Notes:** Covers mandatory 2FA enforcement.

---

## Test Case 5: Reject Registration with Duplicate Email

**Test ID:** TC_005
**Module:** User Management > User Registration
**Category:** Functional
**Priority:** High
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 3 minutes

**Description:** Ensure the system does not allow registration with an email address already in use.

**Objective:** Verify uniqueness constraint on email during registration.

**Preconditions:**
- User with the test email already exists

### Test Steps (Actions Only):

**Step 1:** Navigate to user registration page
**Step 2:** Enter full name
**Step 3:** Enter duplicate email address
**Step 4:** Enter mobile number
**Step 5:** Select user role
**Step 6:** Assign user to group
**Step 7:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Sara Adel |
| email | ahmed.youssef@company.com |
| mobile | 01122334455 |
| role | Verifier |
| group | Custom Collection Group |

**Overall Expected Result:** Registration is blocked with an error message indicating the email is already in use.

**Validation Criteria:**
- Error message is displayed
- No duplicate user is created

**Dependencies:** Existing user with same email

**Notes:** Prevents duplicate user accounts.

---

## Test Case 6: Boundary Test for Mobile Number Length

**Test ID:** TC_006
**Module:** User Management > User Registration
**Category:** Boundary
**Priority:** Medium
**Test Type:** Boundary
**Risk Level:** Low
**Estimated Time:** 4 minutes

**Description:** Test the mobile number field with minimum and maximum allowed lengths.

**Objective:** Ensure mobile number field enforces length constraints.

**Preconditions:**
- Admin user is logged in

### Test Steps (Actions Only):

**Step 1:** Navigate to user registration page
**Step 2:** Enter full name
**Step 3:** Enter mobile number at minimum allowed length
**Step 4:** Enter email address
**Step 5:** Select user role
**Step 6:** Assign user to group
**Step 7:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Khaled Samir |
| mobile | 0101234567 |
| email | khaled.samir@company.com |
| role | Releaser |
| group | Tax Payment Group |

**Overall Expected Result:** Registration is blocked with an error if the mobile number is shorter than required; accepted if at minimum valid length.

**Validation Criteria:**
- Error for too short mobile number
- Acceptance at minimum valid length

**Dependencies:** Mobile number field validation rules

**Notes:** Test with both valid and invalid lengths as separate runs.

---

## Test Case 7: Usability: Clear Button Resets Registration Form

**Test ID:** TC_007
**Module:** User Management > User Registration
**Category:** Usability
**Priority:** Low
**Test Type:** Positive
**Risk Level:** Low
**Estimated Time:** 2 minutes

**Description:** Verify that clicking the clear button resets all fields in the user registration form.

**Objective:** Ensure clear button works as expected for usability.

**Preconditions:**
- Admin user is logged in

### Test Steps (Actions Only):

**Step 1:** Navigate to user registration page
**Step 2:** Enter full name
**Step 3:** Enter email address
**Step 4:** Enter mobile number
**Step 5:** Select user role
**Step 6:** Assign user to group
**Step 7:** Click clear button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Laila Hassan |
| email | laila.hassan@company.com |
| mobile | 01299887766 |
| role | Initiator |
| group | Universal Collection Group |

**Overall Expected Result:** All fields in the registration form are cleared and reset to default values.

**Validation Criteria:**
- All fields are empty after clear
- No residual data remains

**Dependencies:** Registration form available

**Notes:** Improves user experience for data entry.

---

## Test Case 8: Error Message for Missing Mandatory Fields

**Test ID:** TC_008
**Module:** User Management > User Registration
**Category:** Error Handling
**Priority:** Medium
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 3 minutes

**Description:** Ensure that registration cannot proceed if mandatory fields are left blank.

**Objective:** Verify that all mandatory fields are enforced with appropriate error messages.

**Preconditions:**
- Admin user is logged in

### Test Steps (Actions Only):

**Step 1:** Navigate to user registration page
**Step 2:** Leave full name blank
**Step 3:** Enter email address
**Step 4:** Enter mobile number
**Step 5:** Select user role
**Step 6:** Assign user to group
**Step 7:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name |  |
| email | test.user@company.com |
| mobile | 01111222333 |
| role | Verifier |
| group | Tax Payment Group |

**Overall Expected Result:** Registration is blocked with a clear error message indicating that full name is mandatory.

**Validation Criteria:**
- Error message for missing full name
- No user is created

**Dependencies:** Mandatory field validation rules

**Notes:** Repeat for other mandatory fields as needed.

---

## Test Case 9: Performance: Registration Under Load

**Test ID:** TC_009
**Module:** User Management > User Registration
**Category:** Performance
**Priority:** High
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 10 minutes

**Description:** Assess system performance when multiple users are registered simultaneously.

**Objective:** Ensure registration process remains responsive under load.

**Preconditions:**
- Test environment supports concurrent sessions

### Test Steps (Actions Only):

**Step 1:** Open multiple registration forms in parallel sessions
**Step 2:** Enter user details in each session
**Step 3:** Submit registration in all sessions concurrently
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| users | {'full_name': 'User One', 'email': 'user.one@company.com', 'mobile': '01000000001', 'role': 'Initiator', 'group': 'Tax Payment Group'}, {'full_name': 'User Two', 'email': 'user.two@company.com', 'mobile': '01000000002', 'role': 'Verifier', 'group': 'Custom Collection Group'}, {'full_name': 'User Three', 'email': 'user.three@company.com', 'mobile': '01000000003', 'role': 'Approver', 'group': 'Universal Collection Group'} |

**Overall Expected Result:** All users are registered successfully within acceptable response time (e.g., <2 seconds per registration), with no errors or system slowdowns.

**Validation Criteria:**
- All registrations succeed
- Response time is within threshold

**Dependencies:** Load testing tools, Test environment capacity

**Notes:** Simulate at least 3 concurrent registrations.

---

## Test Case 10: Integration: Profile Update Reflected in Authorization Matrix

**Test ID:** TC_010
**Module:** User Management > Profile Management
**Category:** Integration
**Priority:** Medium
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 6 minutes

**Description:** Ensure that changes to user role/group in profile are reflected in the authorization matrix for workflow approvals.

**Objective:** Validate integration between profile management and authorization matrix.

**Preconditions:**
- User exists and is assigned to a workflow

### Test Steps (Actions Only):

**Step 1:** Login as admin user
**Step 2:** Navigate to user management
**Step 3:** Select user to update
**Step 4:** Change user role
**Step 5:** Change user group
**Step 6:** Save profile changes
**Step 7:** Navigate to authorization matrix
**Step 8:** Verify updated user role/group in workflow
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | mohamed.saeed@company.com |
| new_role | Approver |
| new_group | Universal Collection Group |

**Overall Expected Result:** User's updated role and group are reflected in the authorization matrix, and the user is eligible for new workflow approvals accordingly.

**Validation Criteria:**
- Profile updates are reflected in matrix
- User can approve relevant workflows

**Dependencies:** Authorization matrix integration

**Notes:** Ensures profile changes impact workflow as expected.

---

## Test Case 11: Successful Tax Payment File Upload and Processing

**Test ID:** TC_011
**Module:** Tax Collection > File Upload
**Category:** Functional
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 5 minutes

**Description:** Validate that a corporate user can successfully upload a valid tax payment file and the system processes it correctly.

**Objective:** Ensure correct file upload, parsing, and transaction creation for valid files.

**Preconditions:**
- User is logged in with tax payment initiation entitlement
- Tax Collection module is accessible
- Valid payment file is available

### Test Steps (Actions Only):

**Step 1:** Navigate to Tax Collection module
**Step 2:** Select file upload option
**Step 3:** Click upload button
**Step 4:** Select payment file from local system
**Step 5:** Submit file for processing
**Step 6:** Review uploaded file summary
**Step 7:** Confirm file processing
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corpuser1@company.com |
| file_path | /files/valid_tax_payments.csv |
| file_type | csv |
| file_size | 1MB |
| browser | Chrome |
| module | Tax Collection |

**Overall Expected Result:** File is uploaded successfully, parsed without errors, transactions are created and listed for verification, and user receives confirmation message.

**Validation Criteria:**
- File is accepted
- Transactions are created
- No parsing errors
- User receives confirmation

**Dependencies:** Tax Collection module enabled, Valid file format definition

**Notes:** Covers standard file upload and processing scenario.

---

## Test Case 12: File Upload with Invalid Format

**Test ID:** TC_012
**Module:** Custom Collection > File Upload
**Category:** Error Handling
**Priority:** High
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 3 minutes

**Description:** Verify that the system rejects files with unsupported formats during custom collection payment initiation.

**Objective:** Ensure robust validation and error messages for invalid file formats.

**Preconditions:**
- User is logged in with custom collection initiation entitlement
- Custom Collection module is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to Custom Collection module
**Step 2:** Select file upload option
**Step 3:** Click upload button
**Step 4:** Select unsupported file from local system
**Step 5:** Submit file for processing
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corpuser2@company.com |
| file_path | /files/invalid_format_payments.txt |
| file_type | txt |
| file_size | 500KB |
| browser | Firefox |
| module | Custom Collection |

**Overall Expected Result:** System rejects the file upload, displays a clear error message indicating unsupported file format, and does not create any transactions.

**Validation Criteria:**
- File is not accepted
- Appropriate error message displayed
- No transactions created

**Dependencies:** File format validation implemented

**Notes:** Tests error handling for invalid file types.

---

## Test Case 13: API Integration - Fee Retrieval from eFinance

**Test ID:** TC_013
**Module:** Universal Collection > API Integration
**Category:** Integration
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 4 minutes

**Description:** Validate that the system correctly retrieves and displays transaction fees from the eFinance API based on the entered amount.

**Objective:** Ensure accurate fee calculation via external API.

**Preconditions:**
- User is logged in with universal collection initiation entitlement
- eFinance API is available

### Test Steps (Actions Only):

**Step 1:** Navigate to Universal Collection module
**Step 2:** Enter payment amount
**Step 3:** Trigger fee calculation
**Step 4:** Review displayed fee
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corpuser3@company.com |
| amount | 15000 |
| currency | EGP |
| api_endpoint | https://api.efinance.com/fees |
| browser | Edge |

**Overall Expected Result:** Fee is retrieved from eFinance API, displayed accurately on the UI, and matches the expected value for the entered amount.

**Validation Criteria:**
- Fee is displayed
- Value matches API response
- No errors during API call

**Dependencies:** eFinance API operational, Correct API credentials

**Notes:** Validates fee calculation integration.

---

## Test Case 14: API Integration Failure Handling

**Test ID:** TC_014
**Module:** Universal Collection > API Integration
**Category:** Error Handling
**Priority:** High
**Test Type:** Negative
**Risk Level:** High
**Estimated Time:** 3 minutes

**Description:** Verify that the system gracefully handles eFinance API downtime and informs the user appropriately.

**Objective:** Ensure proper error handling and user notification when external API is unavailable.

**Preconditions:**
- User is logged in with universal collection initiation entitlement
- eFinance API is unavailable

### Test Steps (Actions Only):

**Step 1:** Navigate to Universal Collection module
**Step 2:** Enter payment amount
**Step 3:** Trigger fee calculation
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corpuser4@company.com |
| amount | 20000 |
| currency | EGP |
| api_endpoint | https://api.efinance.com/fees |
| api_status | down |
| browser | Chrome |

**Overall Expected Result:** System displays a clear error message indicating fee retrieval failure due to API downtime, and prevents further payment initiation.

**Validation Criteria:**
- Error message displayed
- No payment initiated
- User is informed of the issue

**Dependencies:** API error simulation capability

**Notes:** Tests system resilience to external API failures.

---

## Test Case 15: Role-Based Access Control - Unauthorized File Upload Attempt

**Test ID:** TC_015
**Module:** Tax Collection > Access Control
**Category:** Security
**Priority:** Critical
**Test Type:** Negative
**Risk Level:** Critical
**Estimated Time:** 2 minutes

**Description:** Ensure that users without the required entitlement cannot upload payment files.

**Objective:** Validate RBAC enforcement for file upload actions.

**Preconditions:**
- User is logged in without tax payment initiation entitlement
- Tax Collection module is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to Tax Collection module
**Step 2:** Attempt to access file upload option
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | unauthorizeduser@company.com |
| role | Viewer |
| browser | Safari |
| module | Tax Collection |

**Overall Expected Result:** File upload option is disabled or hidden, and user cannot proceed with uploading files.

**Validation Criteria:**
- Upload option not accessible
- No unauthorized uploads possible

**Dependencies:** RBAC configuration

**Notes:** Validates strict access control for sensitive actions.

---

## Test Case 16: 2FA Enforcement on Payment Approval

**Test ID:** TC_016
**Module:** Universal Collection > Security Validation
**Category:** Security
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 4 minutes

**Description:** Verify that 2FA is enforced during payment approval and only users with valid 2FA can approve transactions.

**Objective:** Ensure strong authentication for critical actions.

**Preconditions:**
- User is logged in with payment approval entitlement
- Pending payment is available for approval

### Test Steps (Actions Only):

**Step 1:** Navigate to Universal Collection module
**Step 2:** Access pending payments
**Step 3:** Select payment for approval
**Step 4:** Initiate approval process
**Step 5:** Enter 2FA code
**Step 6:** Submit approval
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | approver1@company.com |
| payment_id | UC-20240601-001 |
| 2fa_code | 654321 |
| browser | Chrome |

**Overall Expected Result:** 2FA code is validated, payment is approved, and audit log is updated with approval and authentication details.

**Validation Criteria:**
- 2FA required
- Approval succeeds only with valid 2FA
- Audit log updated

**Dependencies:** 2FA service operational, Pending payment exists

**Notes:** Ensures compliance with strong authentication requirements.

---

## Test Case 17: Bulk Verification of Uploaded Payments

**Test ID:** TC_017
**Module:** Custom Collection > Bulk Actions
**Category:** Functional
**Priority:** High
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 5 minutes

**Description:** Validate that users can select and verify multiple uploaded payment transactions in a single bulk action.

**Objective:** Ensure bulk verification functionality works as intended.

**Preconditions:**
- User is logged in with verification entitlement
- Multiple uploaded payments are pending verification

### Test Steps (Actions Only):

**Step 1:** Navigate to Custom Collection module
**Step 2:** Access pending payments list
**Step 3:** Select multiple payments
**Step 4:** Click bulk verify button
**Step 5:** Confirm bulk verification
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | verifier1@company.com |
| payment_ids | CC-20240601-101, CC-20240601-102, CC-20240601-103 |
| browser | Edge |

**Overall Expected Result:** All selected payments are verified in bulk, status is updated, and user receives confirmation for each transaction.

**Validation Criteria:**
- All selected payments verified
- Status updated
- User receives confirmation

**Dependencies:** Bulk verification feature enabled, Pending payments available

**Notes:** Tests efficiency of bulk actions for high-volume users.

---

## Test Case 18: Boundary Test - Maximum File Size for Upload

**Test ID:** TC_018
**Module:** Tax Collection > File Upload
**Category:** Boundary
**Priority:** Medium
**Test Type:** Boundary
**Risk Level:** Medium
**Estimated Time:** 4 minutes

**Description:** Verify that the system accepts a file upload at the maximum allowed file size and rejects files exceeding the limit.

**Objective:** Ensure file size validation works at boundary conditions.

**Preconditions:**
- User is logged in with tax payment initiation entitlement
- Tax Collection module is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to Tax Collection module
**Step 2:** Select file upload option
**Step 3:** Click upload button
**Step 4:** Select file at maximum allowed size
**Step 5:** Submit file for processing
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corpuser5@company.com |
| file_path | /files/max_size_tax_payments.csv |
| file_type | csv |
| file_size | 10MB |
| max_file_size | 10MB |
| browser | Chrome |

**Overall Expected Result:** File at maximum allowed size is accepted and processed successfully; files exceeding the limit are rejected with an appropriate error message.

**Validation Criteria:**
- File at limit accepted
- Oversized files rejected
- Clear error messages

**Dependencies:** File size validation implemented

**Notes:** Validates system behavior at file size boundaries.

---

## Test Case 19: Performance Test - Bulk File Upload Processing Time

**Test ID:** TC_019
**Module:** Universal Collection > File Upload
**Category:** Performance
**Priority:** Medium
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 7 minutes

**Description:** Measure the time taken to upload and process a large bulk payment file and ensure it meets performance requirements.

**Objective:** Ensure system can handle large file uploads within acceptable time limits.

**Preconditions:**
- User is logged in with universal collection initiation entitlement
- Universal Collection module is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to Universal Collection module
**Step 2:** Select file upload option
**Step 3:** Click upload button
**Step 4:** Select large bulk payment file
**Step 5:** Submit file for processing
**Step 6:** Measure processing time until completion
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corpuser6@company.com |
| file_path | /files/large_bulk_payments.csv |
| file_type | csv |
| file_size | 9MB |
| number_of_records | 5000 |
| browser | Firefox |
| performance_threshold | 60 seconds |

**Overall Expected Result:** File is uploaded and processed within 60 seconds, all records are created, and no timeouts or errors occur.

**Validation Criteria:**
- Processing time within threshold
- No errors or timeouts
- All records created

**Dependencies:** Performance monitoring tools available

**Notes:** Assesses system scalability for large uploads.

---

## Test Case 20: Usability - Download and Print Receipt in Arabic

**Test ID:** TC_020
**Module:** Universal Collection > Receipt Management
**Category:** Usability
**Priority:** Low
**Test Type:** Positive
**Risk Level:** Low
**Estimated Time:** 3 minutes

**Description:** Verify that users can download and print payment receipts in Arabic and the content is correctly localized.

**Objective:** Ensure multilingual support and correct formatting for receipts.

**Preconditions:**
- User is logged in with receipt access entitlement
- Payment transaction is completed

### Test Steps (Actions Only):

**Step 1:** Navigate to Universal Collection module
**Step 2:** Access completed payments
**Step 3:** Select payment for receipt
**Step 4:** Choose Arabic language option
**Step 5:** Download receipt
**Step 6:** Print receipt
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corpuser7@company.com |
| payment_id | UC-20240601-201 |
| language | Arabic |
| browser | Chrome |

**Overall Expected Result:** Receipt is downloaded and printed in Arabic, all content is correctly localized, and formatting is preserved.

**Validation Criteria:**
- Receipt in Arabic
- Correct localization
- Proper formatting

**Dependencies:** Arabic localization enabled, Printer configured

**Notes:** Validates multilingual support for end-users.

---

## Test Case 21: Initiate and Approve Tax Payment with Valid Workflow

**Test ID:** TC_021
**Module:** Tax Collection > Payment Workflow
**Category:** Functional
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** Critical
**Estimated Time:** 8 minutes

**Description:** Tests the end-to-end process of initiating and approving a tax payment, ensuring workflow steps and entitlements are enforced.

**Objective:** Validate that tax payment workflow executes correctly with proper entitlements and approvals.

**Preconditions:**
- User is onboarded and assigned to the correct authorization group
- Workflow is configured with initiator, verifier, and approver roles
- User is authenticated with 2FA

### Test Steps (Actions Only):

**Step 1:** Navigate to tax collection module
**Step 2:** Select payment initiation option
**Step 3:** Enter payment details
**Step 4:** Submit payment for verification
**Step 5:** Verify payment as authorized verifier
**Step 6:** Approve payment as authorized approver
**Step 7:** Check transaction status in dashboard
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| tax_type | Income Tax |
| amount | 25000.00 |
| account_number | EG1234567890123456 |
| initiator_username | corp_user1 |
| verifier_username | corp_verifier1 |
| approver_username | corp_approver1 |
| 2fa_code | 123456 |

**Overall Expected Result:** Tax payment is successfully initiated, verified, and approved; transaction status updates to 'Approved' with audit logs reflecting each action; entitlements are enforced at each step.

**Validation Criteria:**
- All workflow steps completed
- Correct entitlements enforced
- Audit logs generated

**Dependencies:** User roles and entitlements configured, Workflow engine operational

**Notes:** Covers standard workflow for tax payment with multi-level approval.

---

## Test Case 22: Error Handling for Invalid Amount in Custom Collection

**Test ID:** TC_022
**Module:** Custom Collection > Payment Initiation
**Category:** Error Handling
**Priority:** High
**Test Type:** Negative
**Risk Level:** High
**Estimated Time:** 3 minutes

**Description:** Verifies system validation and error messaging when a non-numeric or negative amount is entered.

**Objective:** Ensure the system rejects invalid payment amounts and provides clear error messages.

**Preconditions:**
- User is logged in with payment initiation privileges
- Custom collection module is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to custom collection module
**Step 2:** Select payment initiation option
**Step 3:** Enter invalid amount in payment form
**Step 4:** Attempt to submit payment
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| custom_type | Import Duty |
| amount | -5000AB |
| account_number | EG9876543210987654 |
| initiator_username | corp_user2 |

**Overall Expected Result:** System displays validation error indicating invalid amount; payment is not submitted; no transaction is created.

**Validation Criteria:**
- Error message is clear and accurate
- No invalid transaction is created

**Dependencies:** Validation logic implemented for amount fields

**Notes:** Tests numeric and format validation for payment amount.

---

## Test Case 23: Performance Test for Bulk Approval in Universal Collection

**Test ID:** TC_023
**Module:** Universal Collection > Bulk Approval
**Category:** Performance
**Priority:** High
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 10 minutes

**Description:** Measures system response time and success rate when approving a large batch of transactions.

**Objective:** Validate system performance and stability during bulk approval operations.

**Preconditions:**
- User has bulk approval privileges
- At least 100 pending transactions exist

### Test Steps (Actions Only):

**Step 1:** Navigate to universal collection module
**Step 2:** Access pending transactions grid
**Step 3:** Select all transactions for bulk approval
**Step 4:** Initiate bulk approval action
**Step 5:** Monitor system response and completion time
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| approver_username | bulk_approver1 |
| transaction_count | 100 |
| browser | Chrome |
| timeout | 60 seconds |

**Overall Expected Result:** All selected transactions are approved within 60 seconds; system remains responsive; no errors or timeouts occur.

**Validation Criteria:**
- All transactions approved
- Operation completes within timeout
- No system errors

**Dependencies:** Bulk approval feature enabled, Sufficient test data in pending state

**Notes:** Focuses on system scalability and responsiveness under load.

---

## Test Case 24: Database Integrity after Payment Rejection

**Test ID:** TC_024
**Module:** Tax Collection > Payment Workflow
**Category:** Integration
**Priority:** Critical
**Test Type:** Negative
**Risk Level:** Critical
**Estimated Time:** 7 minutes

**Description:** Ensures that rejecting a payment updates all related database records correctly and no orphaned data remains.

**Objective:** Validate data integrity and status updates after payment rejection.

**Preconditions:**
- User is assigned as verifier or approver
- At least one payment is pending verification/approval

### Test Steps (Actions Only):

**Step 1:** Navigate to tax collection module
**Step 2:** Access pending payments list
**Step 3:** Select a pending payment
**Step 4:** Reject the selected payment
**Step 5:** Query database for payment and related audit records
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| payment_id | TXP123456 |
| verifier_username | corp_verifier2 |

**Overall Expected Result:** Payment status is updated to 'Rejected' in the database; all related audit and workflow records reflect the rejection; no orphaned or inconsistent data remains.

**Validation Criteria:**
- Database reflects correct status
- Audit trail is complete
- No orphaned records

**Dependencies:** Database access for validation, Audit logging enabled

**Notes:** Validates backend data integrity after workflow action.

---

## Test Case 25: Unauthorized Access Attempt to Entitlement Management

**Test ID:** TC_025
**Module:** Admin > Entitlement Management
**Category:** Security
**Priority:** Critical
**Test Type:** Negative
**Risk Level:** Critical
**Estimated Time:** 2 minutes

**Description:** Tests system security by attempting to access sensitive entitlement management screens as a non-admin user.

**Objective:** Ensure RBAC prevents unauthorized access to entitlement management.

**Preconditions:**
- User is logged in with standard (non-admin) privileges

### Test Steps (Actions Only):

**Step 1:** Navigate to admin section
**Step 2:** Attempt to access entitlement management page
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corp_user3 |

**Overall Expected Result:** Access is denied; user is shown an authorization error message; no entitlement data is exposed.

**Validation Criteria:**
- Access is blocked
- No sensitive data is leaked

**Dependencies:** RBAC implemented, Entitlement management UI available

**Notes:** Covers security enforcement for admin-only features.

---

## Test Case 26: Boundary Test for Maximum Allowed Payment Amount

**Test ID:** TC_026
**Module:** Universal Collection > Payment Initiation
**Category:** Boundary
**Priority:** High
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 5 minutes

**Description:** Verifies system behavior when initiating a payment at the upper boundary of allowed amount.

**Objective:** Ensure system accepts payment at the maximum allowed limit and processes it correctly.

**Preconditions:**
- User is logged in with payment initiation privileges
- Maximum allowed amount is defined in system configuration

### Test Steps (Actions Only):

**Step 1:** Navigate to universal collection module
**Step 2:** Select payment initiation option
**Step 3:** Enter maximum allowed amount
**Step 4:** Submit payment
**Step 5:** Verify transaction status
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| payment_type | Service Fee |
| amount | 1000000.00 |
| account_number | EG1122334455667788 |
| initiator_username | corp_user4 |

**Overall Expected Result:** Payment is accepted and processed successfully; transaction status is 'Initiated'; no validation errors occur.

**Validation Criteria:**
- Payment is processed at boundary value
- No errors or warnings

**Dependencies:** System configuration for amount limits

**Notes:** Tests upper boundary for payment amount field.

---

## Test Case 27: API Failure Handling During Fee Retrieval

**Test ID:** TC_027
**Module:** Universal Collection > Fee Calculation
**Category:** Integration
**Priority:** High
**Test Type:** Error
**Risk Level:** High
**Estimated Time:** 4 minutes

**Description:** Simulates an external API failure during fee retrieval and verifies system fallback and error messaging.

**Objective:** Ensure system gracefully handles API downtime and informs the user appropriately.

**Preconditions:**
- User is logged in with payment initiation privileges
- eFinance API is intentionally made unavailable

### Test Steps (Actions Only):

**Step 1:** Navigate to universal collection module
**Step 2:** Select payment initiation option
**Step 3:** Enter payment details
**Step 4:** Submit payment to trigger fee retrieval
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| payment_type | License Renewal |
| amount | 500.00 |
| account_number | EG5566778899001122 |
| initiator_username | corp_user5 |

**Overall Expected Result:** System displays an error message indicating fee retrieval failure; payment is not submitted; user is prompted to retry later.

**Validation Criteria:**
- User is informed of API failure
- No incomplete transaction is created

**Dependencies:** eFinance API integration, API can be disabled for testing

**Notes:** Validates error handling for external service unavailability.

---

## Test Case 28: Usability Test for Multilingual Receipt Download

**Test ID:** TC_028
**Module:** Universal Collection > Receipt Management
**Category:** Usability
**Priority:** Medium
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 6 minutes

**Description:** Checks the availability and correctness of downloadable receipts in multiple languages.

**Objective:** Ensure users can download receipts in their preferred language and content is accurate.

**Preconditions:**
- User has completed a successful payment transaction

### Test Steps (Actions Only):

**Step 1:** Navigate to completed transactions list
**Step 2:** Select a completed transaction
**Step 3:** Download receipt in English
**Step 4:** Download receipt in Arabic
**Step 5:** Open and review downloaded receipts
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| transaction_id | UCX987654 |
| user_language_preferences | English, Arabic |

**Overall Expected Result:** Receipts are successfully downloaded in both English and Arabic; all transaction details are accurate and properly localized.

**Validation Criteria:**
- Receipts available in both languages
- Content is accurate and localized

**Dependencies:** Multilingual support enabled, Completed transaction available

**Notes:** Covers multilingual usability for receipt downloads.

---

## Test Case 29: Audit Trail Verification for Entitlement Changes

**Test ID:** TC_029
**Module:** Admin > Entitlement Management
**Category:** Functional
**Priority:** High
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 7 minutes

**Description:** Ensures all changes to user entitlements are logged with complete details for compliance.

**Objective:** Validate that entitlement changes are fully auditable.

**Preconditions:**
- Admin user is logged in
- Audit logging is enabled

### Test Steps (Actions Only):

**Step 1:** Navigate to entitlement management page
**Step 2:** Select a user to modify entitlements
**Step 3:** Change entitlements for the user
**Step 4:** Save changes
**Step 5:** Access audit log viewer
**Step 6:** Search for recent entitlement change entries
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| admin_username | sys_admin1 |
| target_username | corp_user6 |
| entitlement_changes | Add Universal Collection, Remove Custom Collection |

**Overall Expected Result:** All entitlement changes are recorded in the audit log with timestamps, admin user details, and before/after values.

**Validation Criteria:**
- Audit log contains complete details
- All changes are traceable

**Dependencies:** Audit log feature operational

**Notes:** Ensures compliance and traceability for entitlement management.

---

## Test Case 30: Session Timeout Handling During Payment Initiation

**Test ID:** TC_030
**Module:** Universal Collection > Payment Initiation
**Category:** Error Handling
**Priority:** Medium
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 8 minutes

**Description:** Tests system behavior when user session expires during payment initiation.

**Objective:** Ensure incomplete payment is not processed and user is prompted to re-authenticate.

**Preconditions:**
- User is logged in with payment initiation privileges
- Session timeout is configured (e.g., 5 minutes for test)

### Test Steps (Actions Only):

**Step 1:** Navigate to universal collection module
**Step 2:** Select payment initiation option
**Step 3:** Enter payment details
**Step 4:** Remain idle until session timeout occurs
**Step 5:** Attempt to submit payment after timeout
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| payment_type | Utility Bill |
| amount | 750.00 |
| account_number | EG3344556677889900 |
| initiator_username | corp_user7 |
| session_timeout | 5 minutes |

**Overall Expected Result:** User is logged out after timeout; payment is not submitted; user is redirected to login page and prompted to re-authenticate.

**Validation Criteria:**
- Session expires as configured
- No incomplete transaction is processed

**Dependencies:** Session management configured

**Notes:** Validates session management and error handling for idle users.

---

## Test Case 31: Successful Tax Payment Initiation and Approval Workflow

**Test ID:** TC_031
**Module:** Customer Portal > Tax Collection
**Category:** Functional
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** Critical
**Estimated Time:** 10 minutes

**Description:** Validates that a corporate user can initiate a tax payment, and the transaction follows the configured sequential workflow for verification and approval.

**Objective:** Ensure tax payment workflow operates as per configuration, including all required steps and status updates.

**Preconditions:**
- Corporate user is onboarded and entitled for Tax Collection
- Authorization matrix is configured for sequential workflow (Initiator > Verifier > Approver)
- User has sufficient transaction limit

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Navigate to Tax Collection module
**Step 3:** Select 'Initiate New Payment'
**Step 4:** Enter payment details
**Step 5:** Submit payment for verification
**Step 6:** Login as verifier and verify payment
**Step 7:** Login as approver and approve payment
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username_initiator | corpuser1@company.com |
| username_verifier | verifier1@company.com |
| username_approver | approver1@company.com |
| payment_type | Tax |
| tax_id | EG123456789 |
| amount | 50000 |
| currency | EGP |
| payment_date | 05-08-2024 |
| workflow_type | Sequential |

**Overall Expected Result:** Payment is initiated, verified, and approved in sequence; transaction status updates at each stage; audit log records all actions; payment is submitted to core banking integration.

**Validation Criteria:**
- Transaction status changes at each step
- Audit log entries for each action
- Integration call to core banking after approval

**Dependencies:** User entitlement setup, Workflow configuration, Core banking API availability

**Notes:** Covers end-to-end workflow and integration

---

## Test Case 32: Entitlement Misconfiguration - Unauthorized Access Prevention

**Test ID:** TC_032
**Module:** Admin Console > Entitlement Management
**Category:** Security
**Priority:** High
**Test Type:** Negative
**Risk Level:** High
**Estimated Time:** 5 minutes

**Description:** Checks that a user without the required entitlement cannot access or initiate Custom Collection payments.

**Objective:** Validate RBAC enforcement for module access and actions.

**Preconditions:**
- User is onboarded but not entitled for Custom Collection
- Admin has not assigned Custom Collection role to the user

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Attempt to navigate to Custom Collection module
**Step 3:** Attempt to initiate a new payment
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | user2@company.com |
| password | UserPass456! |
| module | Custom Collection |

**Overall Expected Result:** User is denied access to Custom Collection module and cannot initiate payments; appropriate error message is displayed; unauthorized access attempt is logged.

**Validation Criteria:**
- Access is blocked
- Error message is clear
- Audit log records unauthorized attempt

**Dependencies:** Entitlement configuration

**Notes:** Tests RBAC and audit trail for unauthorized access

---

## Test Case 33: Custom Collection Payment - API Fee Retrieval Integration

**Test ID:** TC_033
**Module:** Customer Portal > Custom Collection
**Category:** Integration
**Priority:** High
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 7 minutes

**Description:** Validates that the fee is correctly retrieved from the eFinance API based on the transaction amount during payment initiation.

**Objective:** Ensure fee calculation is accurate and integration is functional.

**Preconditions:**
- User is entitled for Custom Collection
- eFinance API is available

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Navigate to Custom Collection module
**Step 3:** Select 'Initiate New Payment'
**Step 4:** Enter payment details
**Step 5:** Trigger fee retrieval
**Step 6:** Review calculated fee
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | customuser@company.com |
| payment_type | Custom |
| custom_code | CUST2024 |
| amount | 120000 |
| currency | EGP |

**Overall Expected Result:** Fee is retrieved from eFinance API based on amount; fee is displayed to user; payment cannot proceed if API fails or fee is not returned.

**Validation Criteria:**
- Fee matches API response
- Error handling if API fails

**Dependencies:** eFinance API availability

**Notes:** Integration point with external system

---

## Test Case 34: Universal Collection - Mandatory Field Validation

**Test ID:** TC_034
**Module:** Customer Portal > Universal Collection
**Category:** Functional
**Priority:** Medium
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 4 minutes

**Description:** Checks that the system enforces mandatory field validation and displays appropriate error messages.

**Objective:** Ensure data integrity and user guidance for incomplete submissions.

**Preconditions:**
- User is entitled for Universal Collection

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Navigate to Universal Collection module
**Step 3:** Select 'Initiate New Payment'
**Step 4:** Leave mandatory fields blank
**Step 5:** Attempt to submit payment
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | universaluser@company.com |
| fields_left_blank | amount, beneficiary_name |

**Overall Expected Result:** System prevents submission; clear error messages are displayed for each missing mandatory field; no transaction is created.

**Validation Criteria:**
- All mandatory fields are validated
- Error messages are user-friendly

**Dependencies:** Field validation rules

**Notes:** Validates business rules for data entry

---

## Test Case 35: Role Mapping and Authorization Matrix Configuration

**Test ID:** TC_035
**Module:** Admin Console > Role Management
**Category:** Functional
**Priority:** High
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 6 minutes

**Description:** Ensures that admin can create a new role, assign it to a group, and configure approval limits in the authorization matrix.

**Objective:** Validate admin's ability to manage roles and workflow configurations.

**Preconditions:**
- Admin user is logged into the console

### Test Steps (Actions Only):

**Step 1:** Navigate to Role Management section
**Step 2:** Create new role
**Step 3:** Assign role to user group
**Step 4:** Set approval limits in authorization matrix
**Step 5:** Save configuration
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| role_name | HighValueApprover |
| group_name | FinanceManagers |
| approval_limit | 250000 |
| currency | EGP |

**Overall Expected Result:** Role is created and mapped to group; approval limits are set and saved; changes are reflected in authorization matrix and audit log.

**Validation Criteria:**
- Role appears in group mapping
- Approval limits are enforced
- Audit log entry for configuration

**Dependencies:** Admin permissions

**Notes:** Critical for workflow and security configuration

---

## Test Case 36: UI Usability - Navigation and Contextual Help

**Test ID:** TC_036
**Module:** Customer Portal > Navigation
**Category:** Usability
**Priority:** Medium
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 5 minutes

**Description:** Validates the intuitiveness of navigation and the availability of contextual help within the portal.

**Objective:** Ensure users can easily access modules and receive guidance.

**Preconditions:**
- User is onboarded and entitled for all modules

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Navigate to Tax Collection module
**Step 3:** Access contextual help
**Step 4:** Navigate to Custom Collection module
**Step 5:** Access contextual help
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | usabilityuser@company.com |
| modules | Tax Collection, Custom Collection |

**Overall Expected Result:** Navigation is smooth and intuitive; contextual help is available and relevant in each module; no navigation errors occur.

**Validation Criteria:**
- Modules are easily accessible
- Help content is relevant and available

**Dependencies:** Contextual help content

**Notes:** Focus on user experience and guidance

---

## Test Case 37: Boundary Test - Maximum Payment Amount

**Test ID:** TC_037
**Module:** Customer Portal > Tax Collection
**Category:** Boundary
**Priority:** Medium
**Test Type:** Boundary
**Risk Level:** Medium
**Estimated Time:** 4 minutes

**Description:** Tests system behavior when a user attempts to initiate a payment at the maximum allowed limit.

**Objective:** Ensure system enforces upper boundary for payment amount.

**Preconditions:**
- User is entitled for Tax Collection
- Maximum amount is defined in system settings

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Navigate to Tax Collection module
**Step 3:** Select 'Initiate New Payment'
**Step 4:** Enter maximum allowed amount
**Step 5:** Submit payment
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | boundaryuser@company.com |
| amount | 1000000 |
| currency | EGP |
| tax_id | EG987654321 |

**Overall Expected Result:** Payment is accepted and processed if amount equals maximum limit; error is shown if amount exceeds limit.

**Validation Criteria:**
- Boundary is enforced
- No off-by-one errors

**Dependencies:** System configuration for max amount

**Notes:** Validates upper limit enforcement

---

## Test Case 38: Error Handling - External API Downtime During Fee Retrieval

**Test ID:** TC_038
**Module:** Customer Portal > Custom Collection
**Category:** Error Handling
**Priority:** High
**Test Type:** Negative
**Risk Level:** High
**Estimated Time:** 5 minutes

**Description:** Checks system response and error handling when the external fee calculation API is down.

**Objective:** Ensure graceful error handling and user notification for integration failures.

**Preconditions:**
- User is entitled for Custom Collection
- eFinance API is intentionally made unavailable

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Navigate to Custom Collection module
**Step 3:** Select 'Initiate New Payment'
**Step 4:** Enter payment details
**Step 5:** Trigger fee retrieval
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | erroruser@company.com |
| amount | 50000 |
| currency | EGP |
| custom_code | CUSTERR2024 |

**Overall Expected Result:** System displays clear error message about API unavailability; payment cannot proceed; error is logged for monitoring.

**Validation Criteria:**
- Error message is user-friendly
- No incomplete transaction is created
- Error is logged

**Dependencies:** eFinance API downtime simulation

**Notes:** Critical for integration robustness

---

## Test Case 39: Performance Test - Bulk Verification of Pending Transactions

**Test ID:** TC_039
**Module:** Customer Portal > Pending Transactions
**Category:** Performance
**Priority:** Medium
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 8 minutes

**Description:** Assesses system performance and responsiveness during bulk verification operations.

**Objective:** Ensure system can handle bulk actions efficiently without errors or timeouts.

**Preconditions:**
- User is entitled for verification
- Multiple payments are pending verification

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Navigate to Pending Transactions
**Step 3:** Select multiple pending payments
**Step 4:** Initiate bulk verification
**Step 5:** Monitor system response time
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | bulkverifier@company.com |
| pending_payments | TXN1001, TXN1002, TXN1003, TXN1004, TXN1005 |

**Overall Expected Result:** All selected transactions are verified in bulk within acceptable response time; no errors or timeouts occur; audit log records bulk action.

**Validation Criteria:**
- Bulk action completes successfully
- Response time is within SLA
- Audit log entry for bulk verification

**Dependencies:** Bulk verification feature, Sufficient pending transactions

**Notes:** Performance and scalability focus

---

## Test Case 40: Receipt Download and Multilingual Support

**Test ID:** TC_040
**Module:** Customer Portal > Transaction History
**Category:** Usability
**Priority:** Low
**Test Type:** Positive
**Risk Level:** Low
**Estimated Time:** 3 minutes

**Description:** Validates that users can download or print transaction receipts in both supported languages.

**Objective:** Ensure multilingual support and correct receipt formatting.

**Preconditions:**
- User has completed at least one payment transaction

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Navigate to Transaction History
**Step 3:** Select a completed transaction
**Step 4:** Download receipt in English
**Step 5:** Download receipt in Arabic
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | multilingualuser@company.com |
| transaction_id | TXN20240805 |
| languages | English, Arabic |

**Overall Expected Result:** Receipts are downloaded in both English and Arabic; all details are correctly displayed and formatted; language selection works as expected.

**Validation Criteria:**
- Receipts are accurate and readable
- Language switch is functional

**Dependencies:** Multilingual receipt templates

**Notes:** Covers multilingual and print/download features

---

## Test Case 41: Export Tax Collection Report in English as PDF

**Test ID:** TC_041
**Module:** Reporting > Tax Collection Reports
**Category:** Functional
**Priority:** High
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 5 minutes

**Description:** Verify that a corporate user can export a tax collection report in English as a PDF file.

**Objective:** Ensure correct report generation and export functionality for tax collection in English PDF format.

**Preconditions:**
- User is logged in with reporting entitlements
- Tax collection transactions exist for the selected period

### Test Steps (Actions Only):

**Step 1:** Navigate to the Tax Collection Reports section
**Step 2:** Select report type
**Step 3:** Set date range for report
**Step 4:** Choose language option
**Step 5:** Select export format
**Step 6:** Click export button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| report_type | Tax Collection Summary |
| date_from | 01-06-2024 |
| date_to | 30-06-2024 |
| language | English |
| export_format | PDF |

**Overall Expected Result:** A PDF file containing the tax collection summary for the specified date range is downloaded in English, with all transactions and totals accurately displayed.

**Validation Criteria:**
- Report content matches selected criteria
- File is downloadable and opens correctly
- Language is English

**Dependencies:** Tax collection transactions available, User has export permissions

**Notes:** Verify PDF formatting and data accuracy.

---

## Test Case 42: Export Universal Collection Report with Invalid Date Range

**Test ID:** TC_042
**Module:** Reporting > Universal Collection Reports
**Category:** Error Handling
**Priority:** Medium
**Test Type:** Negative
**Risk Level:** Low
**Estimated Time:** 3 minutes

**Description:** Test system response when a user attempts to export a report with an invalid date range.

**Objective:** Validate error handling for invalid date inputs during report export.

**Preconditions:**
- User is logged in with reporting access

### Test Steps (Actions Only):

**Step 1:** Navigate to the Universal Collection Reports section
**Step 2:** Select report type
**Step 3:** Set date range for report
**Step 4:** Choose export format
**Step 5:** Click export button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| report_type | Universal Collection Detailed |
| date_from | 15-07-2024 |
| date_to | 10-07-2024 |
| export_format | Excel |

**Overall Expected Result:** System displays an error message indicating the end date cannot be before the start date, and export is not performed.

**Validation Criteria:**
- Error message is clear and accurate
- No file is exported

**Dependencies:** Date validation logic implemented

**Notes:** Test for both UI and backend validation.

---

## Test Case 43: Verify Backup of Custom Collection Data

**Test ID:** TC_043
**Module:** Backup and Recovery > Data Backup
**Category:** Integration
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 10 minutes

**Description:** Ensure that a scheduled backup of custom collection data completes successfully and data is stored securely.

**Objective:** Validate backup process for custom collection data.

**Preconditions:**
- Custom collection data exists
- User has backup initiation privileges

### Test Steps (Actions Only):

**Step 1:** Navigate to the Backup Management section
**Step 2:** Select data module for backup
**Step 3:** Choose backup type
**Step 4:** Set backup schedule
**Step 5:** Initiate backup process
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| data_module | Custom Collection |
| backup_type | Full |
| schedule | Immediate |

**Overall Expected Result:** Backup completes successfully, backup file is securely stored, and confirmation is logged in the audit trail.

**Validation Criteria:**
- Backup file is created and accessible
- Audit log entry is generated

**Dependencies:** Backup service operational, Sufficient storage available

**Notes:** Test backup integrity in subsequent recovery test.

---

## Test Case 44: Restore Tax Collection Data from Backup

**Test ID:** TC_044
**Module:** Backup and Recovery > Data Recovery
**Category:** Functional
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** Critical
**Estimated Time:** 15 minutes

**Description:** Test the ability to restore tax collection data from a previously created backup file.

**Objective:** Ensure data recovery process works and restores all records accurately.

**Preconditions:**
- Valid backup file exists for tax collection data
- User has recovery permissions

### Test Steps (Actions Only):

**Step 1:** Navigate to the Data Recovery section
**Step 2:** Select backup file for restoration
**Step 3:** Confirm restoration action
**Step 4:** Monitor restoration progress
**Step 5:** Verify completion notification
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| backup_file | tax_collection_backup_20240630.zip |

**Overall Expected Result:** Tax collection data is fully restored from the backup, all records are present and accurate, and a recovery log is generated.

**Validation Criteria:**
- All records restored
- No data loss or corruption
- Recovery log entry created

**Dependencies:** Backup file integrity, Recovery module operational

**Notes:** Cross-verify restored data with backup contents.

---

## Test Case 45: Cross-Platform Export of Custom Collection Report

**Test ID:** TC_045
**Module:** Reporting > Custom Collection Reports
**Category:** Performance
**Priority:** High
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 20 minutes

**Description:** Verify that the custom collection report export works correctly on multiple browsers and operating systems.

**Objective:** Ensure cross-platform compatibility of report export functionality.

**Preconditions:**
- User has access to custom collection reports
- Custom collection data exists

### Test Steps (Actions Only):

**Step 1:** Open the application on the selected platform and browser
**Step 2:** Navigate to Custom Collection Reports section
**Step 3:** Select report type
**Step 4:** Set date range
**Step 5:** Choose export format
**Step 6:** Click export button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| platforms | Windows 11, macOS Ventura, Ubuntu 22.04 |
| browsers | Chrome 125, Firefox 115, Edge 123 |
| report_type | Custom Collection Summary |
| date_from | 01-07-2024 |
| date_to | 10-07-2024 |
| export_format | Excel |

**Overall Expected Result:** Report is exported successfully in Excel format on all tested platforms and browsers, with consistent content and formatting.

**Validation Criteria:**
- Export works on all platforms
- File content and format are identical

**Dependencies:** Application supports all listed browsers and OS, Network connectivity

**Notes:** Compare exported files across platforms for discrepancies.

---

## Test Case 46: Unauthorized User Attempts Data Backup

**Test ID:** TC_046
**Module:** Backup and Recovery > Data Backup
**Category:** Security
**Priority:** High
**Test Type:** Negative
**Risk Level:** High
**Estimated Time:** 3 minutes

**Description:** Test that a user without backup privileges cannot initiate a backup operation.

**Objective:** Ensure proper enforcement of backup privileges.

**Preconditions:**
- User is logged in without backup permissions

### Test Steps (Actions Only):

**Step 1:** Navigate to the Backup Management section
**Step 2:** Attempt to select data module for backup
**Step 3:** Attempt to initiate backup process
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| user_role | Standard Corporate User |
| data_module | Universal Collection |

**Overall Expected Result:** User is denied access to backup functionality, and an appropriate error or access denied message is displayed.

**Validation Criteria:**
- Access is denied
- No backup is initiated
- Error message is clear

**Dependencies:** RBAC implemented for backup operations

**Notes:** Check audit logs for unauthorized attempt.

---

## Test Case 47: Performance of Bulk Report Export

**Test ID:** TC_047
**Module:** Reporting > Bulk Export
**Category:** Performance
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 15 minutes

**Description:** Measure the system's ability to handle bulk export of multiple governmental payment reports.

**Objective:** Validate system performance and stability during bulk export operations.

**Preconditions:**
- User has bulk export privileges
- Multiple report types available

### Test Steps (Actions Only):

**Step 1:** Navigate to the Bulk Export section
**Step 2:** Select multiple report types
**Step 3:** Set date range for all reports
**Step 4:** Choose export format
**Step 5:** Initiate bulk export
**Step 6:** Monitor export progress
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| report_types | Tax Collection, Custom Collection, Universal Collection |
| date_from | 01-06-2024 |
| date_to | 30-06-2024 |
| export_format | PDF |

**Overall Expected Result:** All selected reports are exported successfully within acceptable time limits, with no data loss or system errors.

**Validation Criteria:**
- All reports exported
- Export completes within 2 minutes
- No errors or timeouts

**Dependencies:** Bulk export feature enabled, Sufficient system resources

**Notes:** Monitor system resource usage during export.

---

## Test Case 48: Usability of Data Export Interface for New Users

**Test ID:** TC_048
**Module:** Reporting > Export UI
**Category:** Usability
**Priority:** Medium
**Test Type:** Positive
**Risk Level:** Medium
**Estimated Time:** 7 minutes

**Description:** Assess the usability of the report export interface for a first-time user.

**Objective:** Ensure the export UI is intuitive and user-friendly.

**Preconditions:**
- User account is newly created with reporting access

### Test Steps (Actions Only):

**Step 1:** Log in as a new user
**Step 2:** Navigate to the Reports section
**Step 3:** Attempt to locate export options
**Step 4:** Select report type and date range
**Step 5:** Export the report
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| user_type | First-time Corporate User |
| report_type | Tax Collection |
| date_from | 01-07-2024 |
| date_to | 07-07-2024 |
| export_format | PDF |

**Overall Expected Result:** User is able to easily locate and use the export feature without confusion, and the report is exported successfully.

**Validation Criteria:**
- No user confusion or errors
- Export completes successfully

**Dependencies:** Export UI is deployed, User onboarding completed

**Notes:** Observe user interaction for possible UI improvements.

---

## Test Case 49: Boundary Test: Export Report with Maximum Date Range

**Test ID:** TC_049
**Module:** Reporting > Date Range Validation
**Category:** Boundary
**Priority:** High
**Test Type:** Boundary
**Risk Level:** Medium
**Estimated Time:** 12 minutes

**Description:** Test system behavior when exporting a report with the maximum permitted date range.

**Objective:** Validate system's ability to handle large data exports within boundary limits.

**Preconditions:**
- User has reporting access
- Sufficient data exists for the full date range

### Test Steps (Actions Only):

**Step 1:** Navigate to the Reports section
**Step 2:** Select report type
**Step 3:** Set date range to maximum allowed
**Step 4:** Choose export format
**Step 5:** Click export button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| report_type | Universal Collection |
| date_from | 01-01-2023 |
| date_to | 31-12-2024 |
| export_format | Excel |

**Overall Expected Result:** Report is exported successfully with all data for the maximum date range, no truncation or errors occur.

**Validation Criteria:**
- All data included
- No export errors or timeouts

**Dependencies:** System supports large data exports, Export limits configured

**Notes:** Monitor system performance during export.

---

## Test Case 50: Security Test: Export Attempt Without 2FA

**Test ID:** TC_050
**Module:** Reporting > Export Security
**Category:** Security
**Priority:** Critical
**Test Type:** Negative
**Risk Level:** Critical
**Estimated Time:** 4 minutes

**Description:** Test that a user cannot export reports without completing two-factor authentication.

**Objective:** Ensure 2FA enforcement before allowing report export.

**Preconditions:**
- User account requires 2FA for sensitive actions
- 2FA is not completed

### Test Steps (Actions Only):

**Step 1:** Log in without completing 2FA
**Step 2:** Navigate to the Reports section
**Step 3:** Select report type and date range
**Step 4:** Attempt to export report
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| user_role | Corporate Admin |
| report_type | Tax Collection |
| date_from | 01-06-2024 |
| date_to | 30-06-2024 |
| export_format | PDF |
| 2fa_status | Not Completed |

**Overall Expected Result:** Export is blocked and user is prompted to complete 2FA before proceeding.

**Validation Criteria:**
- Export is blocked
- User receives 2FA prompt

**Dependencies:** 2FA is enforced for report export

**Notes:** Test with both SMS and authenticator app 2FA methods.

---

## Test Case 51: Successful Corporate User Registration

**Test ID:** TC_051
**Module:** User Management > User Registration
**Category:** Functional
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 5 minutes

**Description:** Verify that a corporate user can successfully register by providing all required information with valid data.

**Objective:** Ensure that the registration process works as expected for valid input and creates a new user profile.

**Preconditions:**
- User is not already registered
- Registration page is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to the registration page
**Step 2:** Enter full name
**Step 3:** Enter corporate email address
**Step 4:** Enter mobile number
**Step 5:** Select user role from dropdown
**Step 6:** Set password
**Step 7:** Confirm password
**Step 8:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Ahmed Mostafa |
| email | ahmed.mostafa@company.com |
| mobile | 01234567890 |
| role | Corporate Initiator |
| password | StrongPass!2024 |
| confirm_password | StrongPass!2024 |
| browser | Chrome |
| url | https://vtransact.eg/register |

**Overall Expected Result:** User account is created successfully, confirmation email is sent, and user is redirected to the login page with a success message displayed.

**Validation Criteria:**
- User profile is created in the database
- Confirmation email is received
- Success message is shown

**Dependencies:** Email service operational, Registration page deployed

**Notes:** Covers standard registration workflow for new corporate users.

---

## Test Case 52: Registration with Invalid Email Format

**Test ID:** TC_052
**Module:** User Management > User Registration
**Category:** Functional
**Priority:** High
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 3 minutes

**Description:** Check that the system validates email format and prevents registration with an invalid email.

**Objective:** Ensure email field validation is enforced during registration.

**Preconditions:**
- Registration page is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to the registration page
**Step 2:** Enter full name
**Step 3:** Enter invalid email address
**Step 4:** Enter mobile number
**Step 5:** Select user role from dropdown
**Step 6:** Set password
**Step 7:** Confirm password
**Step 8:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Sara Khaled |
| email | sara.khaled@company |
| mobile | 01122334455 |
| role | Corporate Approver |
| password | Password@2024 |
| confirm_password | Password@2024 |
| browser | Firefox |
| url | https://vtransact.eg/register |

**Overall Expected Result:** Registration is blocked, and a clear error message is displayed indicating invalid email format. No account is created.

**Validation Criteria:**
- Error message is shown for invalid email
- No user account is created

**Dependencies:** Registration page deployed

**Notes:** Validates frontend and backend email format checks.

---

## Test Case 53: Session Timeout After Inactivity

**Test ID:** TC_053
**Module:** Authentication > Session Management
**Category:** Security
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 18 minutes

**Description:** Check if the user is automatically logged out after the configured session timeout period due to inactivity.

**Objective:** Ensure session management enforces automatic logout for security compliance.

**Preconditions:**
- User is logged in
- Session timeout is set to 15 minutes

### Test Steps (Actions Only):

**Step 1:** Login to the portal
**Step 2:** Remain inactive for the session timeout period
**Step 3:** Attempt to perform any action after timeout
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | mona.hassan@company.com |
| password | MonaPass#2024 |
| browser | Edge |
| url | https://vtransact.eg/login |
| timeout | 15 minutes |

**Overall Expected Result:** User is automatically logged out after 15 minutes of inactivity. Any action prompts a login screen and session is terminated.

**Validation Criteria:**
- Session is terminated after timeout
- User is redirected to login screen

**Dependencies:** Session management configured

**Notes:** Validates compliance with security requirements for session handling.

---

## Test Case 54: Login Attempt with Incorrect Password

**Test ID:** TC_054
**Module:** Authentication > Login
**Category:** Security
**Priority:** High
**Test Type:** Negative
**Risk Level:** High
**Estimated Time:** 2 minutes

**Description:** Verify that the system rejects login attempts with incorrect credentials and displays an appropriate error message.

**Objective:** Ensure login security by preventing unauthorized access.

**Preconditions:**
- User account exists

### Test Steps (Actions Only):

**Step 1:** Navigate to login page
**Step 2:** Enter valid username
**Step 3:** Enter incorrect password
**Step 4:** Click login button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | youssef.ali@company.com |
| password | WrongPass123 |
| browser | Chrome |
| url | https://vtransact.eg/login |

**Overall Expected Result:** Login is denied, and a clear error message is displayed indicating incorrect credentials. No session is established.

**Validation Criteria:**
- Error message is shown for wrong password
- No session is created

**Dependencies:** User account exists

**Notes:** Tests password validation and error messaging.

---

## Test Case 55: Mandatory Field Validation During Registration

**Test ID:** TC_055
**Module:** User Management > User Registration
**Category:** Functional
**Priority:** Medium
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 3 minutes

**Description:** Verify that the system enforces mandatory field validation and prevents registration if required fields are left blank.

**Objective:** Ensure data integrity by requiring all mandatory fields during registration.

**Preconditions:**
- Registration page is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to the registration page
**Step 2:** Leave full name field blank
**Step 3:** Enter email address
**Step 4:** Enter mobile number
**Step 5:** Select user role from dropdown
**Step 6:** Set password
**Step 7:** Confirm password
**Step 8:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name |  |
| email | laila.samir@company.com |
| mobile | 01099887766 |
| role | Verifier |
| password | LailaPass!2024 |
| confirm_password | LailaPass!2024 |
| browser | Safari |
| url | https://vtransact.eg/register |

**Overall Expected Result:** Registration is blocked, and an error message is displayed indicating that the full name is required. No user account is created.

**Validation Criteria:**
- Error message for missing mandatory field
- No user account is created

**Dependencies:** Registration page deployed

**Notes:** Validates mandatory field enforcement.

---

## Test Case 56: Password Complexity Enforcement During Registration

**Test ID:** TC_056
**Module:** User Management > User Registration
**Category:** Security
**Priority:** High
**Test Type:** Negative
**Risk Level:** High
**Estimated Time:** 3 minutes

**Description:** Verify that the system enforces password complexity rules and prevents registration with a weak password.

**Objective:** Ensure strong password policies are enforced for user accounts.

**Preconditions:**
- Registration page is accessible

### Test Steps (Actions Only):

**Step 1:** Navigate to the registration page
**Step 2:** Enter full name
**Step 3:** Enter email address
**Step 4:** Enter mobile number
**Step 5:** Select user role from dropdown
**Step 6:** Set weak password
**Step 7:** Confirm password
**Step 8:** Click register button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Omar Fathy |
| email | omar.fathy@company.com |
| mobile | 01211223344 |
| role | Releaser |
| password | 12345 |
| confirm_password | 12345 |
| browser | Chrome |
| url | https://vtransact.eg/register |

**Overall Expected Result:** Registration is blocked, and an error message is displayed indicating password does not meet complexity requirements. No user account is created.

**Validation Criteria:**
- Error message for weak password
- No user account is created

**Dependencies:** Password policy configured

**Notes:** Tests password policy enforcement.

---

## Test Case 57: Profile Update with Valid Data

**Test ID:** TC_057
**Module:** User Management > Profile Management
**Category:** Functional
**Priority:** Medium
**Test Type:** Positive
**Risk Level:** Low
**Estimated Time:** 2 minutes

**Description:** Verify that a user can successfully update their profile details with valid data.

**Objective:** Ensure profile update functionality works as expected for valid input.

**Preconditions:**
- User is logged in

### Test Steps (Actions Only):

**Step 1:** Navigate to profile management page
**Step 2:** Edit full name
**Step 3:** Edit mobile number
**Step 4:** Click save changes button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Omar Fathy ElSayed |
| mobile | 01233445566 |
| browser | Edge |
| url | https://vtransact.eg/profile |

**Overall Expected Result:** Profile is updated successfully, and a confirmation message is displayed. Changes are reflected in the user profile.

**Validation Criteria:**
- Profile data is updated in the database
- Success message is shown

**Dependencies:** User profile exists

**Notes:** Covers standard profile update scenario.

---

## Test Case 58: Profile Update with Invalid Mobile Number

**Test ID:** TC_058
**Module:** User Management > Profile Management
**Category:** Functional
**Priority:** Medium
**Test Type:** Negative
**Risk Level:** Medium
**Estimated Time:** 2 minutes

**Description:** Check that the system validates mobile number format and prevents profile update if the number is invalid.

**Objective:** Ensure data validation for profile fields.

**Preconditions:**
- User is logged in

### Test Steps (Actions Only):

**Step 1:** Navigate to profile management page
**Step 2:** Edit mobile number with invalid format
**Step 3:** Click save changes button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| mobile | 123abc |
| browser | Firefox |
| url | https://vtransact.eg/profile |

**Overall Expected Result:** Profile update is blocked, and an error message is displayed indicating invalid mobile number format. No changes are saved.

**Validation Criteria:**
- Error message for invalid mobile number
- No profile changes are saved

**Dependencies:** User profile exists

**Notes:** Validates input format for mobile number.

---

## Test Case 59: 2FA Authentication During Login

**Test ID:** TC_059
**Module:** Authentication > 2FA Verification
**Category:** Security
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 4 minutes

**Description:** Verify that the system enforces two-factor authentication after successful credential entry.

**Objective:** Ensure enhanced security through 2FA during login.

**Preconditions:**
- User account is enabled for 2FA

### Test Steps (Actions Only):

**Step 1:** Navigate to login page
**Step 2:** Enter valid username
**Step 3:** Enter valid password
**Step 4:** Click login button
**Step 5:** Enter 2FA code received via SMS
**Step 6:** Click verify button
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | fatma.hassan@company.com |
| password | FatmaPass2024! |
| 2fa_code | 856321 |
| browser | Chrome |
| url | https://vtransact.eg/login |

**Overall Expected Result:** User is authenticated and logged in successfully. Dashboard is displayed, and session is established.

**Validation Criteria:**
- 2FA code is required and validated
- User is logged in after successful 2FA

**Dependencies:** 2FA service operational

**Notes:** Validates 2FA enforcement for secure login.

---

## Test Case 60: Performance of Registration Form Submission

**Test ID:** TC_060
**Module:** User Management > User Registration
**Category:** Performance
**Priority:** Medium
**Test Type:** Boundary
**Risk Level:** Medium
**Estimated Time:** 3 minutes

**Description:** Assess the performance of the registration process to ensure it meets acceptable response time criteria.

**Objective:** Ensure registration form submission is performant and does not degrade user experience.

**Preconditions:**
- Registration page is accessible
- Normal system load

### Test Steps (Actions Only):

**Step 1:** Navigate to the registration page
**Step 2:** Enter full name
**Step 3:** Enter email address
**Step 4:** Enter mobile number
**Step 5:** Select user role from dropdown
**Step 6:** Set password
**Step 7:** Confirm password
**Step 8:** Click register button and measure response time
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| full_name | Hossam Tarek |
| email | hossam.tarek@company.com |
| mobile | 01055667788 |
| role | Corporate Initiator |
| password | HossamPass@2024 |
| confirm_password | HossamPass@2024 |
| browser | Chrome |
| url | https://vtransact.eg/register |

**Overall Expected Result:** Registration form submission completes within 2 seconds, and user receives confirmation of successful registration.

**Validation Criteria:**
- Form submission response time is ≤ 2 seconds
- User is registered successfully

**Dependencies:** Performance monitoring tools available

**Notes:** Tests system responsiveness under normal conditions.

---

## Test Case 61: Successful Upload and Processing of Bulk Payment File in Tax Collection Module

**Test ID:** TC_061
**Module:** Tax Collection > File Upload & Document Processing
**Category:** Functional
**Priority:** Critical
**Test Type:** Positive
**Risk Level:** Critical
**Estimated Time:** 10 minutes

**Description:** Validate that a corporate user can successfully upload a valid bulk payment file, and the system processes all records correctly.

**Objective:** Ensure file upload, parsing, and processing work as expected for valid files in the Tax Collection module.

**Preconditions:**
- User is logged in with appropriate entitlements for Tax Collection
- Bulk payment file is prepared in the required format

### Test Steps (Actions Only):

**Step 1:** Navigate to the Tax Collection module
**Step 2:** Select the bulk payment upload option
**Step 3:** Click the upload button
**Step 4:** Select the bulk payment file from local storage
**Step 5:** Submit the file for processing
**Step 6:** Review the processing summary displayed
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corp_user1@company.com |
| file_name | bulk_tax_payments_2024_07.csv |
| file_format | CSV |
| records | {'taxpayer_id': 'EG1234567890', 'amount': '15000.00', 'due_date': '15-07-2024'}, {'taxpayer_id': 'EG0987654321', 'amount': '25000.00', 'due_date': '20-07-2024'} |
| browser | Chrome |
| url | https://vtransact.eg/tax/bulk-upload |

**Overall Expected Result:** File is uploaded successfully, all records are validated and processed, a summary of successful and failed records is displayed, and processed transactions appear in the pending transactions grid.

**Validation Criteria:**
- File accepted and parsed
- All valid records processed
- Processing summary displayed
- Records visible in pending grid

**Dependencies:** Tax Collection module enabled, User has bulk upload entitlement

**Notes:** Test with a valid file containing multiple records to verify end-to-end processing.

---

## Test Case 62: API Integration - Fee Retrieval via eFinance API for Custom Collection

**Test ID:** TC_062
**Module:** Custom Collection > API Integration
**Category:** Integration
**Priority:** High
**Test Type:** Positive
**Risk Level:** High
**Estimated Time:** 5 minutes

**Description:** Verify that the system correctly retrieves and displays transaction fees from the eFinance API based on the entered amount.

**Objective:** Ensure external API integration for fee retrieval works and displays accurate fees.

**Preconditions:**
- User is logged in with access to Custom Collection
- eFinance API is available

### Test Steps (Actions Only):

**Step 1:** Navigate to the Custom Collection module
**Step 2:** Initiate a new payment transaction
**Step 3:** Enter payment amount
**Step 4:** Proceed to fee calculation step
**Step 5:** Review the displayed transaction fee
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | custom_user@company.com |
| amount | 50000.00 |
| currency | EGP |
| api_endpoint | https://api.efinance.eg/fees |
| browser | Firefox |
| url | https://vtransact.eg/custom/initiate |

**Overall Expected Result:** System sends a request to the eFinance API, receives the correct fee for the entered amount, and displays the fee to the user without delay.

**Validation Criteria:**
- API call is made with correct parameters
- Fee is retrieved and displayed accurately

**Dependencies:** eFinance API operational, User has payment initiation entitlement

**Notes:** Monitor API response time and correctness of fee calculation.

---

## Test Case 63: Security Validation - Unauthorized Access Attempt to Admin Entitlement Management

**Test ID:** TC_063
**Module:** Admin > Entitlement Management
**Category:** Security
**Priority:** Critical
**Test Type:** Negative
**Risk Level:** Critical
**Estimated Time:** 3 minutes

**Description:** Ensure that users without admin privileges cannot access or modify entitlement settings.

**Objective:** Validate RBAC implementation and prevent unauthorized access to sensitive admin functions.

**Preconditions:**
- User is logged in with non-admin role

### Test Steps (Actions Only):

**Step 1:** Navigate to the admin section
**Step 2:** Attempt to access the Entitlement Management page
**Step 3:** Try to modify an existing entitlement
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | regular_user@company.com |
| role | CorporateUser |
| target_entitlement | TaxCollectionApproval |
| browser | Edge |
| url | https://vtransact.eg/admin/entitlements |

**Overall Expected Result:** Access is denied at both navigation and modification attempts, with a clear error message indicating insufficient permissions, and no changes are made.

**Validation Criteria:**
- Unauthorized access is blocked
- No entitlement changes possible
- Error message is clear and user-friendly

**Dependencies:** RBAC configured, Non-admin user exists

**Notes:** Test both UI and direct URL access to ensure robust access control.

---

## Test Case 64: Performance - File Upload Timeout Handling in Universal Collection

**Test ID:** TC_064
**Module:** Universal Collection > File Upload
**Category:** Performance
**Priority:** Medium
**Test Type:** Boundary
**Risk Level:** Medium
**Estimated Time:** 7 minutes

**Description:** Check system behavior when uploading a file that exceeds the processing timeout threshold.

**Objective:** Ensure the system gracefully handles file uploads that take too long and provides appropriate feedback.

**Preconditions:**
- User is logged in with Universal Collection access

### Test Steps (Actions Only):

**Step 1:** Navigate to the Universal Collection module
**Step 2:** Select the file upload option
**Step 3:** Click the upload button
**Step 4:** Select a large file from local storage
**Step 5:** Submit the file for upload
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | uni_user@company.com |
| file_name | large_universal_collection_2024_07.csv |
| file_size | 150MB |
| file_format | CSV |
| browser | Chrome |
| url | https://vtransact.eg/universal/upload |
| timeout_threshold | 60 seconds |

**Overall Expected Result:** System detects the upload timeout, aborts the process, displays a timeout error message, and does not process any records from the file.

**Validation Criteria:**
- Timeout is enforced
- User receives clear feedback
- No partial processing occurs

**Dependencies:** Timeout threshold configured, Large test file available

**Notes:** Test with a file size intentionally above the threshold to trigger timeout.

---

## Test Case 65: Usability - Error Handling for Invalid File Format During Payment Upload

**Test ID:** TC_065
**Module:** Tax Collection > File Upload & Document Processing
**Category:** Usability
**Priority:** Low
**Test Type:** Negative
**Risk Level:** Low
**Estimated Time:** 3 minutes

**Description:** Verify that the system detects and handles uploads of unsupported file formats with clear error messages.

**Objective:** Ensure robust error handling and user guidance for invalid file uploads.

**Preconditions:**
- User is logged in with file upload permissions

### Test Steps (Actions Only):

**Step 1:** Navigate to the Tax Collection module
**Step 2:** Select the bulk payment upload option
**Step 3:** Click the upload button
**Step 4:** Select a file with an unsupported format from local storage
**Step 5:** Submit the file for upload
### Test Data (Values Only):

| Field | Value |
|-------|-------|
| username | corp_user2@company.com |
| file_name | invalid_format_bulk_payments_2024_07.txt |
| file_format | TXT |
| browser | Safari |
| url | https://vtransact.eg/tax/bulk-upload |

**Overall Expected Result:** System rejects the upload, displays a clear error message specifying the supported formats, and does not process the file.

**Validation Criteria:**
- Invalid format is detected
- User receives actionable error message
- No processing of invalid files

**Dependencies:** File format validation implemented

**Notes:** Test with a .txt file to verify error handling and user guidance.

---

