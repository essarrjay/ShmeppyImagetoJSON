# **Shmeppy Maps**
This file describes the anatomy of a `.json` shmeppy export map file, which might be useful for those wishing to extend the function of shmeppytools or manually edit files.

# Overview

Shmeppy export maps are a `.json` object with the following structure:

`{"exportFormatVersion":1,"operations":[]}`

`"exportFormatVersion"` appears to be necessary, but there's not need to change the value.

`"operations"` is a list of distinct map related operations (`.json` objects / python dicts), each containing an `id` hash (probably just for "undo/redo" commands, does not need to be unique), and operation `type`.

# Operations

----
## Fill Ops
### Type:FillCells
Uses a single type specific key: "cellFills", which consists of a list of cells.

Each cell takes the form [[x,y], "#hex-color"]

#### Deleting fills
Sets cell's color to null.

#### Examples:  
##### Filling cells
{ "id":"ecb596f5-47f6-4b85-9df8-3d76ca2dc53c",
  "type":"FillCells",
  "cellFills":[
      [[-1,7],"#A0C55F"],
      [[-1,8],"#A0C55F"],
      [[-1,9],"#A0C55F"]
    ]
}

##### Deleting a cell
{"id":"7bb17bf8-a09d-4023-b1a6-c62fbd2be235", "type":"FillCells", "cellFills":[[[-5,-14],null]]}

----

## Edge Ops
### Type:UpdateCellEdges
Uses the same cell structure as with the FillCells op, but the key ("left", "top") describes where that edge should be applied.

In exports, each operation uses only a list of "left" or "top" cells.

No errors are raised if including cells for both "left" and "top" in a single operation.

#### Deleting fills
Sets cell's color to null.

#### Example
{"id":"221b23a1-5279-490d-9d48-049c8ee3be9c",
  "top":[],
  "left":[[[-1,-1],"#EEE"],[[-1,-2],"#EEE"]],
  "type":"UpdateCellEdges"}

----

## **Token Ops**
By far the most complicated set of operations.
Each token is represented by a tokenId (different than the operation id). Subsequent operations acting on that token also include a tokenId value.

### *Type:CreateToken*
#### position
[x,y] coordinate position of the token
#### color
hex color value of token color (str)

#### Example
{ "id":"a6d9e419-aadd-4452-b434-a9dff58bab8a",
  "type":"CreateToken",
  "color":"#A0C55F",
  "tokenId":"d45446d4-5401-4922-9365-f43684ccefb0",
  "position":[1,-10]}

### *Type:MoveToken*
#### position
[x,y] new coordinate position of the token

#### Example
{"id":"f9baa776-7e5d-49f6-b37f-1d66de5c22f0",
"type":"MoveToken",
"tokenId":"6e29a2f2-a138-4a04-8a58-d462324e7f8b",
"position":[-21,-8]}

### *Type:ResizeToken*

#### width, height
the new size of the token

#### x, y
used when the token's position is changed when resizing. For example a 2x2 token is shrunk from upper left to lower right.

#### Example
{"y":-1,
"x":-1,
"id":"b7b47876-b03f-434a-bab9-9ecf26ac00ea",
"type":"ResizeToken",
"width":1,
"height":1,
"tokenId":"beba9c5c-ece2-480b-8c5c-401d2b877717"}

### Type:UpdateTokenLabel
#### label
A string of the label text

#### Example
{"id":"4457b999-3c0b-4fab-bf19-897669311764","type":"UpdateTokenLabel","label":"Ernesto","tokenId":"189e35e3-98e7-4734-99da-c60b31f647e4"}

### Type:DeleteToken
Merely names the token id to be deleted.

{"id":"0dc73b4a-6241-430d-ad4a-32e9358720a8","type":"DeleteToken","tokenId":"9ada8c2a-0a72-4940-885b-f90ddbeb9130"}

----

## **Fog of War Ops**
### Type:UpdateHiddenCells
Two lists of positions [x,y] indicating which cellsToHide and which cellsToShow

#### Example:  
{"id":"c7d99733-332f-48b7-a8e7-a1349f751c65","type":"UpdateHiddenCells","cellsToHide":[],"cellsToShow":[[-1,10],[-1,7],[-1,8],[-1,9]]}

## Other Ops
Update Title (of map)
