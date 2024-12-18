# <div align="center"> TINY language Parser and Scanner </div>

## 1. <u>**Project description**</u>
- Given the TINY grammar rules you should implement the TINY parser using recursive descent method.
- You will need to convert grammar into EBNF form.
- The output will be a complete syntax tree of the input source program

## 2. <u>**Inputs**</u>
List of ( tokenvalue, tokentype) in a file

Examples:
- x , Identifier
- :=, assign
- 4,number

The input list should follow the same syntax as mentioned in the previous example (tokenvalue , tokentype)

Input list can be input through GUI textbox or by loading a text file

### <u>**List of token types in tiny language**</u>

| TokenType     | Value/Example |
|:------------- | ------------- |
| SEMICOLON     | ;             |
| IF            | if            |
| THEN          | then          |
| END           | end           |
| REPEAT        | repeat        |
| UNTIL         | until         |
| IDENTIFIER    | x - abc - xyz |
| ASSIGN        | :=            |
| READ          | read          |
| WRITE         | write         |
| LESSTHAN      | <             |
| EQUAL         | =             |
| PLUS          | +             |
| MINUS         | -             |
| MULT          | *             |
| DIV           | /             |
| OPENBRACKET   | (             |
| CLOSEDBRACKET | )             |
| NUMBER        | 12 - 289      |


## 3. <u>**Output**</u>
1. State whether the statements are accepted by TINY language or not
2. Draw Syntax tree on a GUI based application
3. IF you do not support GUI ( and will lose GUI marks) you can output recognized structures by the TINY language parser into a file or on the console screen ( like drawing the syntax tree by describing it using statement names)

## 4. <u>**Examples**</u>
------
### Example 1
```
{ Sample program in TINY language computes factorial }
read x; {input an integer}
if 0 < x then {don't compute if x <= 0}
	fact := 1;
	repeat
		fact := fact * x;
		x := x - 1
	until x = 0;
	write fact {output factorial of x}
end
```
![example 1 scanner](images/Example1%20scanner.jpeg)
![example 1 parser](/images/Example1%20parser.jpeg)
