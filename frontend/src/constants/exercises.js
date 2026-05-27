export const EXERCISES = {
  Python: [
    {
      question: "What is the correct way to check if a number is even?",
      options: ["if num % 2 == 0:", "if num / 2 == 0:", "if num // 2 == 0:", "if num % 2 = 0:"],
      correct: 0,
      explanation: "The modulo operator % gives the remainder. If num % 2 equals 0, the number is even."
    },
    {
      question: "Which function reads user input in Python?",
      options: ["input()", "read()", "scan()", "get_input()"],
      correct: 0,
      explanation: "input() reads a line from the user and returns it as a string."
    },
    {
      question: "What does len() return for the string 'hello'?",
      options: ["4", "5", "6", "undefined"],
      correct: 1,
      explanation: "len('hello') returns 5 because the string has 5 characters."
    },
    {
      question: "Which keyword defines a function in Python?",
      options: ["function", "def", "define", "func"],
      correct: 1,
      explanation: "Python uses the def keyword to define functions."
    },
    {
      question: "What error occurs when you divide by zero?",
      options: ["ValueError", "TypeError", "ZeroDivisionError", "IndexError"],
      correct: 2,
      explanation: "Dividing by zero raises a ZeroDivisionError in Python."
    }
  ],
  JavaScript: [
    {
      question: "Which keyword declares a constant variable in JavaScript?",
      options: ["var", "let", "const", "static"],
      correct: 2,
      explanation: "const declares a variable that cannot be reassigned."
    },
    {
      question: "What does typeof null return?",
      options: ["null", "undefined", "object", "boolean"],
      correct: 2,
      explanation: "typeof null returns 'object' — this is a well-known JavaScript bug from the language's early days."
    },
    {
      question: "How do you write a comment in JavaScript?",
      options: ["# comment", "// comment", "<!-- comment -->", "/* comment"],
      correct: 1,
      explanation: "JavaScript uses // for single-line comments."
    },
    {
      question: "What is the correct way to declare a function?",
      options: ["function myFunc() {}", "def myFunc() {}", "func myFunc() {}", "create myFunc() {}"],
      correct: 0,
      explanation: "The function keyword is used to declare functions in JavaScript."
    },
    {
      question: "Which method adds an element to the end of an array?",
      options: ["push()", "pop()", "shift()", "unshift()"],
      correct: 0,
      explanation: "push() adds one or more elements to the end of an array and returns the new length."
    }
  ],
  TypeScript: [
    {
      question: "How do you specify a variable can be string or number?",
      options: ["let x: string | number;", "let x: string || number;", "let x: [string, number];", "let x: any;"],
      correct: 0,
      explanation: "Union types use the | symbol to allow multiple types."
    },
    {
      question: "What does the ? mean in 'name?: string'?",
      options: ["Required parameter", "Optional parameter", "Nullable parameter", "Default parameter"],
      correct: 1,
      explanation: "The ? marks the parameter as optional — it can be omitted when calling the function."
    },
    {
      question: "Which access modifier makes a member visible only within its own class?",
      options: ["public", "private", "protected", "readonly"],
      correct: 1,
      explanation: "The 'private' modifier restricts access to the class itself — subclasses and external code cannot access private members."
    }
  ],
  "C++": [
    {
      question: "What header is needed for input/output in C++?",
      options: ["<stdio.h>", "<iostream>", "<string>", "<cmath>"],
      correct: 1,
      explanation: "#include <iostream> provides cin, cout, and other I/O functionality."
    },
    {
      question: "Which operator allocates memory on the heap?",
      options: ["malloc", "alloc", "new", "create"],
      correct: 2,
      explanation: "The new operator allocates memory on the heap and calls the constructor."
    },
    {
      question: "What does the ++ operator do?",
      options: ["Adds 2", "Increments by 1", "Decrements by 1", "Multiplies by 2"],
      correct: 1,
      explanation: "++ increments a variable by 1. x++ is equivalent to x = x + 1."
    }
  ],
  Java: [
    {
      question: "What is the entry point of a Java program?",
      options: ["public void main(String[] args)", "public static void main(String[] args)", "static void main(String[] args)", "public main(String[] args)"],
      correct: 1,
      explanation: "The exact signature must be public static void main(String[] args) for the JVM to find it."
    },
    {
      question: "Which keyword is used to inherit a class?",
      options: ["inherits", "extends", "implements", "using"],
      correct: 1,
      explanation: "extends is used for class inheritance in Java."
    },
    {
      question: "What is null in Java?",
      options: ["0", "undefined", "A special literal meaning no value", "An empty string"],
      correct: 2,
      explanation: "null is a special literal that represents the absence of a value for reference types."
    }
  ],
  Go: [
    {
      question: "How do you declare a variable in Go?",
      options: ["var x int = 5", "x := 5", "Both are valid", "let x = 5"],
      correct: 2,
      explanation: "Go supports both 'var x int = 5' and short declaration 'x := 5'."
    },
    {
      question: "What is the zero value of an int in Go?",
      options: ["null", "undefined", "0", "nil"],
      correct: 2,
      explanation: "In Go, integers have a zero value of 0. nil is for pointers, slices, maps, etc."
    },
    {
      question: "How do you handle errors in Go?",
      options: ["try/catch", "if err != nil", "error()", "handle error"],
      correct: 1,
      explanation: "Go uses explicit error checking with 'if err != nil' rather than exceptions."
    }
  ],
  Rust: [
    {
      question: "What keyword declares a variable as mutable in Rust?",
      options: ["var", "mut", "let", "changeable"],
      correct: 1,
      explanation: "Variables in Rust are immutable by default. Use 'mut' to make them mutable."
    },
    {
      question: "What is the String type in Rust?",
      options: ["str", "String", "string", "char[]"],
      correct: 1,
      explanation: "String is a growable, heap-allocated UTF-8 string. &str is a string slice."
    },
    {
      question: "Which macro prints to the console in Rust?",
      options: ["print()", "console.log()", "println!()", "echo()"],
      correct: 2,
      explanation: "println!() is a macro that prints text followed by a newline."
    }
  ],
  C: [
    {
      question: "What is the correct return type for main()?",
      options: ["void", "int", "float", "char"],
      correct: 1,
      explanation: "Standard C requires main() to return int. 'void main()' is not standard."
    },
    {
      question: "Which function reads formatted input in C?",
      options: ["read()", "scanf()", "input()", "gets()"],
      correct: 1,
      explanation: "scanf() reads formatted input from stdin. It needs the address of variables with &."
    },
    {
      question: "What does the & operator do?",
      options: ["Logical AND", "Bitwise AND", "Address-of operator", "Reference operator"],
      correct: 2,
      explanation: "The & operator returns the memory address of a variable."
    }
  ],
  Dart: [
    {
      question: "What keyword declares a variable in Dart?",
      options: ["var", "let", "const", "All of the above"],
      correct: 3,
      explanation: "Dart supports var, final, and const for variable declarations."
    },
    {
      question: "What is the entry point of a Dart program?",
      options: ["public static void main()", "void main()", "main()", "start()"],
      correct: 2,
      explanation: "Dart uses main() as the entry point. It can return void and take optional parameters."
    }
  ],
  Ruby: [
    {
      question: "How do you define a method in Ruby?",
      options: ["function method_name", "def method_name", "define method_name", "method method_name"],
      correct: 1,
      explanation: "Ruby uses 'def' to define methods, similar to Python."
    },
    {
      question: "What does nil represent in Ruby?",
      options: ["Empty string", "Zero", "Absence of value", "Undefined variable"],
      correct: 2,
      explanation: "nil is an object representing the absence of a value. It is the only instance of NilClass."
    }
  ],
  PHP: [
    {
      question: "How do you echo output in PHP?",
      options: ["print()", "echo", "write()", "Both echo and print"],
      correct: 3,
      explanation: "Both echo and print can output text in PHP. echo is marginally faster."
    },
    {
      question: "Which symbol starts a variable name in PHP?",
      options: ["@", "$", "#", "&"],
      correct: 1,
      explanation: "All PHP variables start with $, like $name, $count, etc."
    }
  ],
  Swift: [
    {
      question: "How do you declare a constant in Swift?",
      options: ["const", "let", "var", "final"],
      correct: 1,
      explanation: "Swift uses 'let' for constants and 'var' for variables."
    },
    {
      question: "What is an optional in Swift?",
      options: ["A required parameter", "A type that can hold a value or nil", "A default value", "An error type"],
      correct: 1,
      explanation: "Optionals (Type?) represent values that may be nil. You unwrap them with ! or if-let."
    }
  ],
  Kotlin: [
    {
      question: "How do you declare a variable in Kotlin?",
      options: ["var x = 5", "let x = 5", "x := 5", "Both var and val"],
      correct: 3,
      explanation: "Kotlin uses 'val' for read-only and 'var' for mutable variables."
    },
    {
      question: "What does ?. (safe call operator) do?",
      options: ["Calls method only if not null", "Always calls method", "Throws on null", "Creates nullable type"],
      correct: 0,
      explanation: "The safe call operator ?. calls the method only if the object is not null."
    }
  ],
  "C#": [
    {
      question: "Which keyword marks a method as async in C#?",
      options: ["async", "await", "task", "parallel"],
      correct: 0,
      explanation: "The async keyword marks a method as asynchronous. Await is used inside async methods."
    },
    {
      question: "What is the base class for all types in C#?",
      options: ["Object", "Base", "ValueType", "System"],
      correct: 0,
      explanation: "System.Object is the ultimate base class for all types in C#."
    }
  ],
  SQL: [
    {
      question: "Which statement deletes rows from a table?",
      options: ["DELETE FROM", "REMOVE FROM", "DROP FROM", "CLEAR FROM"],
      correct: 0,
      explanation: "DELETE FROM removes rows from a table. Always use a WHERE clause to avoid deleting all rows."
    },
    {
      question: "How do you check for NULL in SQL?",
      options: ["= NULL", "== NULL", "IS NULL", "EQUALS NULL"],
      correct: 2,
      explanation: "Use IS NULL or IS NOT NULL. = NULL does not work because NULL is not a value."
    },
    {
      question: "Which clause filters grouped data?",
      options: ["WHERE", "HAVING", "FILTER", "GROUP BY"],
      correct: 1,
      explanation: "HAVING filters groups after GROUP BY. WHERE filters rows before grouping."
    }
  ],
  HTML: [
    {
      question: "Which tag creates a hyperlink?",
      options: ["<link>", "<a>", "<href>", "<url>"],
      correct: 1,
      explanation: "The <a> tag (anchor) creates hyperlinks. The href attribute specifies the URL."
    },
    {
      question: "What does <!DOCTYPE html> do?",
      options: ["Creates an HTML element", "Declares the document type", "Imports CSS", "Defines the title"],
      correct: 1,
      explanation: "<!DOCTYPE html> tells the browser to use modern standards mode instead of quirks mode."
    },
    {
      question: "Which tag is self-closing?",
      options: ["<div>", "<p>", "<img>", "<h1>"],
      correct: 2,
      explanation: "<img> is a void element — it does not need a closing tag."
    }
  ],
  CSS: [
    {
      question: "How do you select an element by its ID?",
      options: [".myId", "#myId", "[myId]", "*myId"],
      correct: 1,
      explanation: "The # prefix selects an element by its id attribute."
    },
    {
      question: "Which property makes a layout flexible?",
      options: ["display: block", "display: flex", "display: grid", "display: inline"],
      correct: 1,
      explanation: "display: flex creates a flexible box layout for arranging items in rows or columns."
    },
    {
      question: "What CSS unit is relative to the parent's font-size?",
      options: ["px", "rem", "em", "vh"],
      correct: 2,
      explanation: "em is relative to the parent element's font-size. rem is relative to the root font-size."
    }
  ]
};

export const LANGUAGE_WEAKNESS_MAP = {
  Python: ["Loop logic", "Null / zero handling", "Variable scoping"],
  JavaScript: ["Variable scoping", "Type coercion", "Async patterns"],
  TypeScript: ["Type definitions", "Union types", "Generics"],
  "C++": ["Null / zero handling", "Memory management", "Pointer arithmetic"],
  Java: ["Null / zero handling", "Exception handling", "Generics"],
  Go: ["Error handling", "Interface design", "Goroutine sync"],
  Rust: ["Borrow checker", "Lifetime annotations", "Ownership"],
  C: ["Null / zero handling", "Pointer arithmetic", "Memory management"],
  Dart: ["Null safety", "Async/await", "Type system"],
  Ruby: ["Block syntax", "Symbols vs strings", "Method visibility"],
  PHP: ["Type juggling", "Array functions", "Namespace resolution"],
  Swift: ["Optional unwrapping", "Protocol conformance", "Memory management"],
  Kotlin: ["Null safety", "Coroutines", "Extension functions"],
  "C#": ["Async/await", "LINQ queries", "Delegate syntax"],
  SQL: ["Join types", "NULL handling", "Query optimization"],
  HTML: ["Semantic tags", "Form attributes", "Accessibility"],
  CSS: ["Flexbox", "Grid layout", "Responsive design"]
};
