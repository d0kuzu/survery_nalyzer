from mods import *

wb = a.load_workbook("./open.xlsx")
sheet = wb.worksheets[0]

lastQuest = ''
for row in range(2, sheet.max_row):
    answers.append({})
    for col in sheet.columns:
        if col[0].value is not None and col[1].value is not None:
            answers[row-2][f'{col[0].value}'] = {f'{col[1].value}': col[row].value}
            lastQuest = col[0].value
        elif col[0].value is None:
            answers[row-2][f'{lastQuest}'][f'{col[1].value}'] = col[row].value
wb.close()
# for i in answers:
#     print(f'{i}')

# cols={'byXP': '', 'bySEX': '', 'byAGE': '', 'byEMP': ''}
# for i in answers[0]:
#     if cols['byXP']=='' and i.lower().find('работ') != -1:
#         cols['byXP']=i
#     if cols['bySEX']=='' and i.lower().find('пол') != -1:
#         cols['bySEX']=i
#     if cols['byAGE']=='' and i.lower().find('возраст') != -1:
#         cols['byAGE']=i
#     if cols['byEMP']=='' and i.lower().find('подчин') != -1:
#         cols['byEMP']=i

SetTables()

from newVisual import main

main.root.mainloop()
