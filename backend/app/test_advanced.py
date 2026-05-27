"""Advanced multi-language test suite — edge cases, false positives, diverse patterns."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from analyzer import analyze_code

passed = 0
failed = 0

def check(desc, code, lang, expect_errors=None, expect_no_errors=None,
          expect_suggestions=None, expect_errors_count=None):
    global passed, failed
    r = analyze_code(code, lang)
    got = {e['type'] for e in r['errors']}
    suggestion_titles = {s['title'] for s in r.get('suggestions', [])}
    ok = True
    msg = f"[{lang}] {desc}"

    if expect_errors:
        missing = set(expect_errors) - got
        if missing:
            ok = False
            print(f"  FAIL {msg}: missing errors {missing}")

    if expect_no_errors:
        found = got & set(expect_no_errors)
        if found:
            ok = False
            print(f"  FAIL {msg}: unexpected errors {found}")

    if expect_errors_count is not None:
        if len(r['errors']) != expect_errors_count:
            ok = False
            print(f"  FAIL {msg}: expected {expect_errors_count} errors, got {len(r['errors'])}")

    if expect_suggestions is not None:
        missing_sug = set(expect_suggestions) - suggestion_titles
        if missing_sug:
            ok = False
            print(f"  FAIL {msg}: missing suggestions {missing_sug}")

    if ok:
        passed += 1
        print(f"  OK {msg}")
    else:
        failed += 1

# ===========================================================================
# PYTHON — advanced
# ===========================================================================
print("\n=== PYTHON (advanced) ===")

check("type hints no false positive", 'def add(x: int, y: int) -> int:\n    return x + y', 'python',
      expect_no_errors={"NameError", "SyntaxError", "ZeroDivisionError"})

check("f-strings no false positive", 'name = "world"\nprint(f"hello {name}")', 'python',
      expect_no_errors={"NameError"})

check("list comprehension clean", 'squares = [x**2 for x in range(10)]', 'python',
      expect_no_errors={"NameError", "UndefinedIterable"})

check("walrus operator", 'if (n := len("hi")) > 0:\n    print(n)', 'python',
      expect_no_errors={"AssignmentInCondition", "NameError"})

check("decorator no false pos", 'def dec(f):\n    def wrapper():\n        return f()\n    return wrapper\n\n@dec\ndef foo():\n    pass', 'python',
      expect_no_errors={"NameError", "SyntaxError"})

check("generator no false pos", 'def gen():\n    for i in range(5):\n        yield i', 'python',
      expect_no_errors={"InfiniteLoopError", "NameError"})

check("context manager", 'with open("f.txt") as f:\n    data = f.read()', 'python',
      expect_no_errors={"NameError"})

check("lambda no false pos", 'f = lambda x: x + 1\nprint(f(5))', 'python',
      expect_no_errors={"NameError"})

check("match/case (3.10+) syntax", 'def parse(x):\n    match x:\n        case 1:\n            return "one"\n        case _:\n            return "other"', 'python',
      expect_no_errors={"SyntaxError"})

check("missing return in function", 'def add(a, b):\n    result = a + b', 'python',
      expect_errors={"MissingReturn"})

check("variable shadowing", 'x = 10\ndef foo(x):\n    return x', 'python',
      expect_suggestions={"Variable Shadowing"})

check("dead code after return", 'def foo():\n    return 5\n    x = 10', 'python',
      expect_errors={"DeadCode"})

check("possible recursion", 'def foo():\n    return foo()', 'python',
      expect_suggestions={"Possible Accidental Recursion"})

check("threading no false pos", 'import threading\nt = threading.Thread(target=print)\nt.start()', 'python',
      expect_no_errors={"NameError", "InfiniteLoopError", "ZeroDivisionError"})

check("exception handling", 'try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    x = 0', 'python',
      expect_no_errors={"BareExcept", "ZeroDivisionError"})

check("class method self", 'class Foo:\n    def __init__(self, x):\n        self.x = x\n    def get(self):\n        return self.x', 'python',
      expect_no_errors={"NameError", "Unused Variable"})

check("dict comprehension", 'd = {k: v for k, v in [("a", 1)]}', 'python',
      expect_no_errors={"NameError", "UndefinedIterable"})

check("async function", 'async def fetch():\n    return 42', 'python',
      expect_no_errors={"SyntaxError"})

check("inheritance", 'class Animal:\n    def speak(self): pass\nclass Dog(Animal):\n    def speak(self): return "woof"', 'python',
      expect_no_errors={"NameError"})

# ===========================================================================
# JAVASCRIPT — advanced
# ===========================================================================
print("\n=== JAVASCRIPT (advanced) ===")

check("arrow function", 'const add = (a, b) => a + b;', 'javascript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

check("promise chain", 'fetch("/api")\n  .then(r => r.json())\n  .then(d => console.log(d));', 'javascript',
      expect_no_errors={"MissingSemicolon"})

check("async/await", 'async function get() {\n  const r = await fetch("/api");\n  return r.json();\n}', 'javascript',
      expect_no_errors={"LooseEquality", "MissingSemicolon"})

check("destructuring", 'const [a, b] = [1, 2];\nconst {x, y} = {x: 1, y: 2};', 'javascript',
      expect_no_errors={"MissingSemicolon"})

check("template literal", 'const name = "world";\nconst msg = `hello ${name}`;', 'javascript',
      expect_no_errors={"MissingSemicolon"})

check("class definition", 'class Foo {\n  constructor(x) {\n    this.x = x;\n  }\n  getX() { return this.x; }\n}', 'javascript',
      expect_no_errors={"MissingSemicolon"})

check("spread operator", 'const arr = [1, 2, 3];\nconst copy = [...arr];', 'javascript',
      expect_no_errors={"MissingSemicolon"})

check("closure", 'function makeCounter() {\n  let count = 0;\n  return function() { return ++count; };\n}', 'javascript',
      expect_no_errors={"MissingSemicolon"})

check("module import/export", 'import { foo } from "./bar.js";\nexport const baz = 5;', 'javascript',
      expect_no_errors={"MissingSemicolon"})

check("null check no false pos", 'if (x !== null && x !== undefined) {}', 'javascript',
      expect_no_errors={"LooseEquality"})

check("for-of loop", 'for (const item of items) {\n  console.log(item);\n}', 'javascript',
      expect_no_errors={"MissingSemicolon"})

check("object method shorthand", 'const obj = {\n  foo() { return 1; },\n  bar: 2\n};', 'javascript',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# TYPESCRIPT — advanced
# ===========================================================================
print("\n=== TYPESCRIPT (advanced) ===")

check("interface", 'interface User {\n  name: string;\n  age: number;\n}\nconst u: User = { name: "a", age: 5 };', 'typescript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

check("generics", 'function identity<T>(arg: T): T { return arg; }', 'typescript',
      expect_no_errors={"MissingSemicolon"})

check("enum", 'enum Color { Red, Green, Blue }\nconst c: Color = Color.Red;', 'typescript',
      expect_no_errors={"MissingSemicolon"})

check("union type", 'let x: string | number = "hello";', 'typescript',
      expect_no_errors={"MissingSemicolon"})

check("type alias", 'type Point = { x: number; y: number };\nconst p: Point = { x: 0, y: 0 };', 'typescript',
      expect_no_errors={"MissingSemicolon"})

check("async with type", 'async function fetchData(): Promise<string> {\n  return "data";\n}', 'typescript',
      expect_no_errors={"MissingSemicolon"})

check("decorator syntax", 'function log(target: any, key: string) {}\nclass Foo {\n  @log\n  method() {}\n}', 'typescript',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# C — advanced
# ===========================================================================
print("\n=== C (advanced) ===")

check("struct definition", 'struct Point {\n  int x;\n  int y;\n};', 'c',
      expect_no_errors={"MissingSemicolon"})

check("function pointer", 'int (*cmp)(const void*, const void*);', 'c',
      expect_no_errors={"MissingSemicolon"})

check("typedef", 'typedef unsigned long ulong;\nulong x = 5;', 'c',
      expect_no_errors={"MissingSemicolon"})

check("union", 'union Data {\n  int i;\n  float f;\n};', 'c',
      expect_no_errors={"MissingSemicolon"})

check("enum", 'enum Color { RED, GREEN, BLUE };\nenum Color c = RED;', 'c',
      expect_no_errors={"MissingSemicolon"})

check("#define macro", '#define MAX(a,b) ((a)>(b)?(a):(b))\nint x = MAX(3, 5);', 'c',
      expect_no_errors={"SyntaxError"})

check("do-while loop", 'int i = 0;\ndo {\n  i++;\n} while (i < 10);', 'c',
      expect_no_errors={"MissingSemicolon"})

check("ternary no false pos", 'int x = a > b ? a : b;', 'c',
      expect_no_errors={"AssignmentInCondition"})

check("goto", 'int main() {\n  goto end;\n  end:\n  return 0;\n}', 'c',
      expect_no_errors={"MissingSemicolon", "SyntaxError"})

check("nested comments", 'int main() {\n  /* outer /* inner */\n  return 0;\n}', 'c',
      expect_no_errors={"SyntaxError"})

check("static array no false pos", 'int arr[] = {1, 2, 3};', 'c',
      expect_no_errors={"BufferUnderflow", "BufferOverflow"})

check("string literal as arg", 'printf("hello");', 'c',
      expect_no_errors={"FormatMismatch"})

check("multi-declaration", 'int a, b, c;', 'c',
      expect_no_errors={"MissingSemicolon"})

check("access struct member via .", 'struct Point p;\np.x = 5;\np.y = 10;', 'c',
      expect_no_errors={"NullPointerDereference"})

check("compound literal", 'int *p = (int[]){1, 2, 3};', 'c',
      expect_no_errors={"MissingSemicolon"})

check("array of pointers", 'char *names[] = {"a", "b", "c"};', 'c',
      expect_no_errors={"WildPointer"})

# ===========================================================================
# C++ — advanced
# ===========================================================================
print("\n=== C++ (advanced) ===")

check("class with constructor", 'class Foo {\npublic:\n  Foo(int x) : x_(x) {}\nprivate:\n  int x_;\n};', 'c++',
      expect_no_errors={"MissingSemicolon"})

check("template function", 'template<typename T>\nT max(T a, T b) { return a > b ? a : b; }', 'c++',
      expect_no_errors={"MissingSemicolon"})

check("STL vector", '#include <vector>\nstd::vector<int> v = {1, 2, 3};', 'c++',
      expect_no_errors={"MissingSemicolon"})

check("smart pointer", '#include <memory>\nstd::unique_ptr<int> p = std::make_unique<int>(5);', 'c++',
      expect_no_errors={"MemoryLeak", "MissingNullCheck"})

check("reference", 'void swap(int &a, int &b) {\n  int t = a;\n  a = b;\n  b = t;\n}', 'c++',
      expect_no_errors={"WildPointer"})

check("namespace", 'namespace mylib {\n  int add(int a, int b) { return a + b; }\n}', 'c++',
      expect_no_errors={"MissingSemicolon"})

check("virtual function", 'class Base {\npublic:\n  virtual void foo() {}\n};\nclass Derived : public Base {\npublic:\n  void foo() override {}\n};', 'c++',
      expect_no_errors={"MissingSemicolon"})

check("exception try-catch", '#include <stdexcept>\nint main() {\n  try {\n    throw std::runtime_error("err");\n  } catch (const std::exception& e) {\n    return 1;\n  }\n  return 0;\n}', 'c++',
      expect_no_errors={"MissingSemicolon"})

check("lambda C++11", 'auto f = [](int x) { return x + 1; };', 'c++',
      expect_no_errors={"MissingSemicolon"})

check("constexpr with recursion", 'constexpr int factorial(int n) {\n  return n <= 1 ? 1 : n * factorial(n - 1);\n}', 'c++',
      expect_no_errors={"MissingSemicolon"}, expect_errors_count=1)

check("move semantics", 'std::vector<int> v = std::move(other);', 'c++',
      expect_no_errors={"MissingSemicolon"})

check("operator overloading", 'struct Vec {\n  int x, y;\n  Vec operator+(const Vec& o) const {\n    return {x + o.x, y + o.y};\n  }\n};', 'c++',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# C# — advanced
# ===========================================================================
print("\n=== C# (advanced) ===")

check("namespace and class", 'namespace App {\n  class Program {\n    static void Main() {}\n  }\n}', 'c#',
      expect_no_errors={"MissingSemicolon"})

check("properties", 'class Person {\n  public string Name { get; set; }\n}', 'c#',
      expect_no_errors={"MissingSemicolon"})

check("LINQ query", 'using System.Linq;\nvar q = from x in items where x > 5 select x;', 'c#',
      expect_no_errors={"MissingSemicolon"})

check("async/await C#", 'async Task<int> GetAsync() {\n  await Task.Delay(100);\n  return 42;\n}', 'c#',
      expect_no_errors={"MissingSemicolon"})

check("event/delegate", 'public delegate void Handler(object sender);\npublic event Handler Click;', 'c#',
      expect_no_errors={"MissingSemicolon"})

check("generic method", 'T Identity<T>(T arg) { return arg; }', 'c#',
      expect_no_errors={"MissingSemicolon"})

check("lambda C#", 'Func<int, int> f = x => x + 1;', 'c#', expect_no_errors={"MissingSemicolon"})

check("string interpolation", 'string s = $"Hello {name}";', 'c#',
      expect_no_errors={"MissingSemicolon"})

check("null-conditional", 'int? len = name?.Length;', 'c#',
      expect_no_errors={"MissingSemicolon"})

check("record type C# 9", 'public record Person(string Name, int Age);', 'c#',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# DART — advanced
# ===========================================================================
print("\n=== DART (advanced) ===")

check("class and constructor", 'class Foo {\n  int x;\n  Foo(this.x);\n}', 'dart',
      expect_no_errors={"MissingSemicolon"})

check("null safety", 'String? name;\nint len = name?.length ?? 0;', 'dart',
      expect_no_errors={"MissingSemicolon"})

check("async/await Dart", 'Future<int> get() async {\n  await Future.delayed(Duration(seconds: 1));\n  return 42;\n}', 'dart',
      expect_no_errors={"MissingSemicolon"})

check("arrow function Dart", 'int add(int a, int b) => a + b;', 'dart',
      expect_no_errors={"MissingSemicolon"})

check("collection literals", 'var list = [1, 2, 3];\nvar map = {"a": 1};', 'dart',
      expect_no_errors={"MissingSemicolon"})

check("mixin", 'mixin Flyable {\n  void fly() {}\n}\nclass Bird with Flyable {}', 'dart',
      expect_no_errors={"MissingSemicolon"})

check("extension method", 'extension on String {\n  int get charCount => length;\n}', 'dart',
      expect_no_errors={"MissingSemicolon"})

check("factory constructor", 'class Foo {\n  factory Foo.fromJson(Map json) {\n    return Foo();\n  }\n  Foo();\n}', 'dart',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# JAVA — advanced
# ===========================================================================
print("\n=== JAVA (advanced) ===")

check("package and import", 'package com.example;\nimport java.util.List;\nclass Foo {}', 'java',
      expect_no_errors={"MissingSemicolon"})

check("lambda Java", 'List<Integer> nums = Arrays.asList(1, 2, 3);\nnums.forEach(n -> System.out.println(n));', 'java',
      expect_no_errors={"MissingSemicolon"})

check("stream API", 'int sum = list.stream().filter(x -> x > 0).mapToInt(x -> x).sum();', 'java',
      expect_no_errors={"MissingSemicolon"})

check("generics Java", 'class Box<T> {\n  T value;\n  void set(T v) { value = v; }\n  T get() { return value; }\n}', 'java',
      expect_no_errors={"MissingSemicolon"})

check("annotation", '@Override\npublic String toString() { return ""; }', 'java',
      expect_no_errors={"MissingSemicolon"})

check("abstract class", 'abstract class Shape {\n  abstract double area();\n}', 'java',
      expect_no_errors={"MissingSemicolon"})

check("enum Java", 'enum Status { PENDING, ACTIVE, DONE }', 'java',
      expect_no_errors={"MissingSemicolon"})

check("static import", 'import static java.lang.Math.PI;', 'java',
      expect_no_errors={"MissingSemicolon"})

check("var keyword Java 10", 'var list = new ArrayList<String>();', 'java',
      expect_no_errors={"MissingSemicolon"})

check("synchronized method", 'class Counter {\n  int count;\n  synchronized void inc() { count++; }\n}', 'java',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# KOTLIN — advanced
# ===========================================================================
print("\n=== KOTLIN (advanced) ===")

check("null safety Kotlin", 'var name: String? = null\nval len = name?.length ?: 0', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

check("extension function", 'fun String.exclaim() = this + "!"', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

check("data class", 'data class User(val name: String, val age: Int)', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

check("lambda Kotlin", 'val sum = { x: Int, y: Int -> x + y }', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

check("string templates", 'val msg = "Hello ${name}"', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

check("sealed class", 'sealed class Result\ndata class Success(val data: String) : Result()', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

check("companion object", 'class Foo {\n  companion object {\n    const val ID = 1\n  }\n}', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

check("coroutine", 'suspend fun fetch(): String {\n  delay(100)\n  return "ok"\n}', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# GO — advanced
# ===========================================================================
print("\n=== GO (advanced) ===")

check("goroutine", 'package main\nfunc main() {\n  go fmt.Println("hi")\n}', 'go',
      expect_no_errors={"MissingSemicolon"})

check("channel", 'package main\nfunc main() {\n  ch := make(chan int)\n  go func() { ch <- 42 }()\n  <-ch\n}', 'go',
      expect_no_errors={"MissingSemicolon"})

check("defer", 'package main\nfunc main() {\n  f, _ := os.Open("f.txt")\n  defer f.Close()\n}', 'go',
      expect_no_errors={"MissingSemicolon"})

check("interface Go", 'type Shape interface {\n  Area() float64\n}', 'go',
      expect_no_errors={"MissingSemicolon"})

check("method Go", 'type Point struct { X, Y float64 }\nfunc (p Point) Dist() float64 { return math.Sqrt(p.X*p.X + p.Y*p.Y) }', 'go',
      expect_no_errors={"MissingSemicolon"})

check("slice and map", 'package main\nvar s = []int{1, 2, 3}\nvar m = map[string]int{"a": 1}', 'go',
      expect_no_errors={"MissingSemicolon"})

check("struct tags", 'type User struct {\n  Name string `json:"name"`\n  Age  int    `json:"age"`\n}', 'go',
      expect_no_errors={"MissingSemicolon"})

check("error handling Go", 'f, err := os.Open("f.txt")\nif err != nil {\n  return err\n}', 'go',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# RUST — advanced
# ===========================================================================
print("\n=== RUST (advanced) ===")

check("ownership move", 'fn main() {\n  let s = String::from("hello");\n  let t = s;\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("borrowing", 'fn main() {\n  let s = String::from("hello");\n  let len = calculate_length(&s);\n}\nfn calculate_length(s: &String) -> usize { s.len() }', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("lifetime annotation", "fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {\n  if x.len() > y.len() { x } else { y }\n}", 'rust',
      expect_no_errors={"MissingSemicolon"})

check("pattern matching", 'fn main() {\n  match x {\n    1 => println!("one");\n    _ => println!("other");\n  }\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("Result type", 'fn div(a: f64, b: f64) -> Result<f64, String> {\n  if b == 0.0 { Err("div by zero".into()) }\n  else { Ok(a / b) }\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("Option type", 'fn maybe_num() -> Option<i32> {\n  return Some(42);\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("impl block", 'struct Rectangle { width: u32, height: u32 }\nimpl Rectangle {\n  fn area(&self) -> u32 { self.width * self.height }\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("closure Rust", 'fn main() {\n  let add = |a, b| a + b;\n  println!("{}", add(2, 3));\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("trait", 'trait Speak {\n  fn speak(&self) -> String;\n}\nstruct Dog;\nimpl Speak for Dog {\n  fn speak(&self) -> String { "woof".into() }\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("vector macro", 'fn main() {\n  let v = vec![1, 2, 3];\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

check("if let", 'fn main() {\n  if let Some(x) = maybe_val {\n    println!("{}", x);\n  }\n}', 'rust',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# SWIFT — advanced
# ===========================================================================
print("\n=== SWIFT (advanced) ===")

check("optionals Swift", 'var name: String? = nil\nif let n = name {\n  print(n)\n}', 'swift',
      expect_no_errors={"MissingSemicolon"})

check("closure Swift", 'let add = { (a: Int, b: Int) -> Int in a + b }', 'swift',
      expect_no_errors={"MissingSemicolon"})

check("struct Swift", 'struct Point {\n  var x: Double\n  var y: Double\n}', 'swift',
      expect_no_errors={"MissingSemicolon"})

check("protocol", 'protocol Speakable {\n  func speak() -> String\n}', 'swift',
      expect_no_errors={"MissingSemicolon"})

check("extension", 'extension String {\n  var reversed: String { return String(self.reversed()) }\n}', 'swift',
      expect_no_errors={"MissingSemicolon"})

check("guard let", 'func greet(name: String?) {\n  guard let n = name else { return }\n  print("Hello \(n)")\n}', 'swift',
      expect_no_errors={"MissingSemicolon"})

check("enum with associated", 'enum Result {\n  case success(Data)\n  case failure(Error)\n}', 'swift',
      expect_no_errors={"MissingSemicolon"})

check("throws function", 'func parse() throws -> String {\n  return "ok"\n}', 'swift',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# SQL — advanced
# ===========================================================================
print("\n=== SQL (advanced) ===")

check("JOIN", 'SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

check("GROUP BY HAVING", 'SELECT dept, COUNT(*) FROM employees GROUP BY dept HAVING COUNT(*) > 5', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

check("subquery", 'SELECT * FROM users WHERE id IN (SELECT user_id FROM orders)', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

check("aggregate functions", 'SELECT MAX(salary), MIN(salary), AVG(salary) FROM employees', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

check("CREATE TABLE", 'CREATE TABLE users (\n  id INT PRIMARY KEY,\n  name VARCHAR(100)\n)', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

check("INSERT with columns", 'INSERT INTO users (id, name) VALUES (1, \'Alice\')', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

check("transaction", 'BEGIN TRANSACTION;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nCOMMIT;', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

check("ALTER TABLE", 'ALTER TABLE users ADD COLUMN email VARCHAR(255)', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

check("WHERE with IS NULL", 'SELECT * FROM users WHERE email IS NULL', 'sql',
      expect_no_errors={"NullComparison"})

# ===========================================================================
# HTML — advanced
# ===========================================================================
print("\n=== HTML (advanced) ===")

check("DOCTYPE + html", '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <title>Page</title>\n</head>\n<body>content</body>\n</html>', 'html',
      expect_no_errors={"MissingDoctype", "SyntaxError"})

check("form elements", '<form action="/submit" method="POST">\n  <input type="text" name="name">\n  <button type="submit">Go</button>\n</form>', 'html',
      expect_no_errors={"SyntaxError"})

check("table structure", '<table>\n  <tr><th>Name</th><th>Age</th></tr>\n  <tr><td>Alice</td><td>30</td></tr>\n</table>', 'html',
      expect_no_errors={"SyntaxError"})

check("semantic elements", '<header>head</header>\n<main>\n  <article>\n    <section>content</section>\n  </article>\n</main>\n<footer>foot</footer>', 'html',
      expect_no_errors={"SyntaxError", "MissingDoctype"})

check("ARIA attributes", '<div role="button" aria-label="close" tabindex="0">X</div>', 'html',
      expect_no_errors={"SyntaxError"})

check("meta viewport", '<meta name="viewport" content="width=device-width, initial-scale=1">', 'html',
      expect_no_errors={"SyntaxError"})

check("data attributes", '<div data-user-id="42" data-role="admin">content</div>', 'html',
      expect_no_errors={"SyntaxError"})

check("nested lists", '<ul>\n  <li>Item 1\n    <ul><li>Subitem</li></ul>\n  </li>\n</ul>', 'html',
      expect_no_errors={"SyntaxError"})

check("iframe", '<iframe src="https://example.com" title="example"></iframe>', 'html',
      expect_no_errors={"SyntaxError"})

check("script tag", '<script src="app.js" defer></script>', 'html',
      expect_no_errors={"SyntaxError"})

# ===========================================================================
# CSS — advanced
# ===========================================================================
print("\n=== CSS (advanced) ===")

check("animation keyframes", '@keyframes slide {\n  from { transform: translateX(0); }\n  to { transform: translateX(100px); }\n}\n.foo { animation: slide 2s; }', 'css',
      expect_no_errors={"InvalidColorValue"})

check("media query", '@media (max-width: 768px) {\n  body { font-size: 14px; }\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("flexbox", '.container {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  gap: 10px;\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("CSS grid", '.grid {\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  gap: 20px;\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("custom properties (vars)", ':root {\n  --primary: #007bff;\n  --spacing: 16px;\n}\n.foo {\n  color: var(--primary);\n  margin: var(--spacing);\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("calc()", '.foo {\n  width: calc(100% - 40px);\n  height: calc(100vh - 60px);\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("gradient", '.foo {\n  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("box-shadow", '.foo {\n  box-shadow: 0 2px 4px rgba(0,0,0,.1);\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("pseudo-classes", 'a:hover { color: red; }\nli:nth-child(odd) { background: #f0f0f0; }\ninput:focus { border-color: blue; }', 'css',
      expect_no_errors={"InvalidColorValue"})

check("pseudo-elements", 'p::before { content: ">> "; }\np::after { content: " <<"; }\n::selection { background: yellow; }', 'css',
      expect_no_errors={"InvalidColorValue"})

check("transform", '.foo {\n  transform: translate(10px, 20px) rotate(45deg) scale(1.5);\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("transition", '.foo {\n  transition: all 0.3s ease-in-out;\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("font-face", '@font-face {\n  font-family: "Custom";\n  src: url("font.woff2");\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("multiple selectors", 'h1, h2, h3 {\n  font-family: sans-serif;\n  line-height: 1.4;\n}', 'css',
      expect_no_errors={"InvalidColorValue"})

check("named color", '.foo { color: transparent; background: papayawhip; }', 'css',
      expect_no_errors={"InvalidColorValue"})

# ===========================================================================
# SUMMARY
# ===========================================================================
print(f"\n{'='*60}")
print(f"Passed: {passed}/{passed+failed}")
if failed:
    print(f"FAILED: {failed}")
else:
    print("All advanced tests passed!")

if failed:
    sys.exit(1)
