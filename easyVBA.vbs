'This is the code for the easy version of assignment 2

Sub easyVBA()

'create variable to store values for total volume, ticker name, each row per ticker, etc.
dim ticker_name as String
dim total_volume as Double
total_volume = 0
dim Summary_Table_row as Integer
Summary_Table_row = 2

'create headers for ticker and total stock volume
Cells(1,9).Value = "Ticker"
Cells(1,10).Value = "Total Stock Volume"

'create an if then statement that will push the collected total to the appropriate column with its ticker
'if the next ticker is not equal to the current one
For i = 2 to 43398
    If Cells(i + 1, 1).Value <> Cells(i, 1).Value Then
        ticker_name = Cells(i, 1).Value
        total_volume = total_volume + Cells(i, 7).Value
        Range("I" & Summary_Table_row).Value = ticker_name
        Range("J" & Summary_Table_row).Value = total_volume
        Summary_Table_row = Summary_Table_row + 1
        total_volume = 0
    Else
        total_volume = total_volume + Cells(i, 7).Value
    End If
Next i 

'autofit columns for neatness
columns.Autofit

End Sub