# import pandas as pd
# from openpyxl import Workbook
# from openpyxl.styles import Font, Alignment, PatternFill
#
#
# def generate_test_case_excel(test_cases: list, output_path: str):
#     """Generate Excel file from test cases"""
#     try:
#         if not test_cases:
#             # Create empty workbook with headers
#             wb = Workbook()
#             ws = wb.active
#             ws.title = "Test Cases"
#
#             headers = ["Test ID", "Test Name", "Description", "Preconditions",
#                        "Test Steps", "Expected Result", "Priority", "Category", "Risk Level"]
#
#             for col, header in enumerate(headers, 1):
#                 ws.cell(row=1, column=col, value=header)
#
#             wb.save(output_path)
#             return
#
#         # Convert test cases to DataFrame
#         df_data = []
#         for tc in test_cases:
#             # Handle test_steps list
#             test_steps_text = ""
#             if isinstance(tc.get('test_steps'), list):
#                 test_steps_text = '\n'.join([f"{i + 1}. {step}" for i, step in enumerate(tc.get('test_steps', []))])
#             else:
#                 test_steps_text = str(tc.get('test_steps', ''))
#
#             df_data.append({
#                 'Test ID': tc.get('test_id', ''),
#                 'Test Name': tc.get('test_name', ''),
#                 'Description': tc.get('description', ''),
#                 'Preconditions': tc.get('preconditions', ''),
#                 'Test Steps': test_steps_text,
#                 'Expected Result': tc.get('expected_result', ''),
#                 'Priority': tc.get('priority', ''),
#                 'Category': tc.get('category', ''),
#                 'Risk Level': tc.get('risk_level', '')
#             })
#
#         df = pd.DataFrame(df_data)
#
#         # Create Excel file with formatting
#         with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#             df.to_excel(writer, sheet_name='Test Cases', index=False)
#
#             # Get the workbook and worksheet
#             workbook = writer.book
#             worksheet = writer.sheets['Test Cases']
#
#             # Format headers
#             header_font = Font(bold=True, color="FFFFFF")
#             header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
#
#             for col in range(1, len(df.columns) + 1):
#                 cell = worksheet.cell(row=1, column=col)
#                 cell.font = header_font
#                 cell.fill = header_fill
#                 cell.alignment = Alignment(horizontal="center", vertical="center")
#
#             # Adjust column widths
#             column_widths = {
#                 'A': 10,  # Test ID
#                 'B': 25,  # Test Name
#                 'C': 40,  # Description
#                 'D': 20,  # Preconditions
#                 'E': 50,  # Test Steps
#                 'F': 30,  # Expected Result
#                 'G': 12,  # Priority
#                 'H': 15,  # Category
#                 'I': 12  # Risk Level
#             }
#
#             for col, width in column_widths.items():
#                 worksheet.column_dimensions[col].width = width
#
#             # Enable text wrapping for all cells
#             for row in worksheet.iter_rows():
#                 for cell in row:
#                     cell.alignment = Alignment(wrap_text=True, vertical="top")
#
#     except Exception as e:
#         raise Exception(f"Failed to generate Excel file: {str(e)}")
#
