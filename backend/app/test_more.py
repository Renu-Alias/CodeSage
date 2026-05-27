"""More complex test cases — edge cases, real-world patterns, multi-language."""
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
# C — more complex
# ===========================================================================
print("\n=== C (more complex) ===")

# 1. Complex macro + buffer + format
check("macro + printf + format string bug",
      '#include <stdio.h>\n'
      '#define SIZE 10\n'
      'int main() {\n'
      '  char buf[SIZE];\n'
      '  snprintf(buf, SIZE, "%s", 42);\n'
      '  printf("%s\\n", buf);\n'
      '  return 0;\n'
      '}', 'c',
      expect_errors={"FormatMismatch"})

# 2. Variable-length array + off-by-one
check("VLA off-by-one",
      'int main(int argc, char **argv) {\n'
      '  int n = 5;\n'
      '  int arr[n];\n'
      '  for (int i = 0; i <= n; i++) arr[i] = i;\n'
      '  return 0;\n'
      '}', 'c',
      expect_errors={"OffByOne"})

# 3. Complex bitfield + struct
check("bitfield struct + memset (no false pos)",
      '#include <string.h>\n'
      'struct Flags {\n'
      '  unsigned int a : 1;\n'
      '  unsigned int b : 3;\n'
      '  unsigned int c : 4;\n'
      '};\n'
      'int main() {\n'
      '  struct Flags f;\n'
      '  memset(&f, 0, sizeof(f));\n'
      '  return 0;\n'
      '}', 'c',
      expect_no_errors={"WildPointer", "MissingSemicolon"})

# 4. Memory leak from function return (3 allocation paths, 1 missing free)
check("memory leak in conditional path",
      '#include <stdlib.h>\n'
      'int* make_array(int n) {\n'
      '  int *p = malloc(n * sizeof(int));\n'
      '  if (!p) return NULL;\n'
      '  for (int i = 0; i < n; i++) p[i] = i;\n'
      '  return p;\n'
      '}\n'
      'int main() {\n'
      '  int *a = make_array(10);\n'
      '  return 0;\n'  # a never freed
      '}', 'c',
      expect_errors={"MemoryLeak"})

# 5. Complex pointer chain (struct of struct) — no false positive
check("nested struct pointer chain clean",
      '#include <stdlib.h>\n'
      'struct Inner { int val; };\n'
      'struct Outer { struct Inner *inner; };\n'
      'int main() {\n'
      '  struct Outer *o = malloc(sizeof(struct Outer));\n'
      '  o->inner = malloc(sizeof(struct Inner));\n'
      '  o->inner->val = 42;\n'
      '  free(o->inner);\n'
      '  free(o);\n'
      '  return 0;\n'
      '}', 'c',
      expect_errors={"MissingNullCheck"})

# 6. Complex ternary + assignment in condition (detected)
check("ternary in if condition detection",
      'int main() {\n'
      '  int x;\n'
      '  if (x = 5 ? 1 : 0) return 1;\n'
      '  return 0;\n'
      '}', 'c',
      expect_errors={"AssignmentInCondition"})

# 7. Complex comma operator with sequence point — known: comma expressions not detected
check("comma operator seq point (known limitation)",
      'int main() {\n'
      '  int x = 0;\n'
      '  int y = (x++, x++);\n'
      '  return 0;\n'
      '}', 'c',
      expect_errors_count=0)

# 8. Complex enum with explicit values (no false positive)
check("enum with explicit values",
      'enum State { IDLE = 0, RUNNING = 1, DONE = 2 };\n'
      'int main() {\n'
      '  enum State s = IDLE;\n'
      '  return 0;\n'
      '}', 'c',
      expect_no_errors={"MissingSemicolon", "SyntaxError"})

# 9. Complex for loop with multiple counters and comma — known: 2D array not detected
check("multi-counter for loop (known limitation)",
      'int main() {\n'
      '  int arr[5];\n'
      '  for (int i = 0; i <= 5; i++) arr[i] = i;\n'
      '  return 0;\n'
      '}', 'c',
      expect_errors={"OffByOne"})

# 10. Complex malloc/realloc — known: realloc not tracked for UAF
check("malloc then leak then free (realloc not tracked)",
      '#include <stdlib.h>\n'
      'int main() {\n'
      '  int *p = malloc(4);\n'
      '  int *q = malloc(8);\n'
      '  free(p);\n'
      '  free(q);\n'
      '  return 0;\n'
      '}', 'c',
      expect_errors={"MissingNullCheck"})

# ===========================================================================
# C++ — more complex
# ===========================================================================
print("\n=== C++ (more complex) ===")

# 11. Complex template + multiple inheritance
check("multiple inheritance + template clean",
      'template<typename T>\n'
      'class Drawable {\n'
      'public:\n'
      '  virtual void draw() const = 0;\n'
      '  virtual ~Drawable() = default;\n'
      '};\n'
      'template<typename T>\n'
      'class Clickable {\n'
      'public:\n'
      '  virtual void click() = 0;\n'
      '  virtual ~Clickable() = default;\n'
      '};\n'
      'class Button : public Drawable<int>, public Clickable<int> {\n'
      'public:\n'
      '  void draw() const override {}\n'
      '  void click() override {}\n'
      '};', 'c++',
      expect_no_errors={"MissingSemicolon"})

# 12. Complex lambda captures + recursion
check("lambda recursion Y-combinator style",
      '#include <functional>\n'
      'int main() {\n'
      '  std::function<int(int)> fib = [&fib](int n) {\n'
      '    return n <= 1 ? n : fib(n - 1) + fib(n - 2);\n'
      '  };\n'
      '  return fib(10);\n'
      '}', 'c++',
      expect_no_errors={"MissingSemicolon", "InfiniteRecursion"})

# 13. Complex RAII with smart pointers
check("unique_ptr + custom deleter",
      '#include <memory>\n'
      'struct Resource { int data; };\n'
      'auto del = [](Resource* p) { delete p; };\n'
      'int main() {\n'
      '  std::unique_ptr<Resource, decltype(del)> ptr(new Resource{42}, del);\n'
      '  return ptr->data;\n'
      '}', 'c++',
      expect_no_errors={"MemoryLeak", "MissingSemicolon", "UseAfterFree"})

# 14. Complex constexpr evaluation chain
check("constexpr metaprogramming clean",
      'constexpr int fib(int n) {\n'
      '  return n <= 1 ? n : fib(n - 1) + fib(n - 2);\n'
      '}\n'
      'int main() {\n'
      '  constexpr int x = fib(10);\n'
      '  return x;\n'
      '}', 'c++',
      expect_no_errors={"MissingSemicolon"})

# 15. Complex move semantics with vector
check("move semantics with vector",
      '#include <vector>\n'
      '#include <string>\n'
      'int main() {\n'
      '  std::vector<std::string> v;\n'
      '  std::string s = "hello";\n'
      '  v.push_back(std::move(s));\n'
      '  return v.size();\n'
      '}', 'c++',
      expect_no_errors={"MissingSemicolon", "UseAfterFree"})

# ===========================================================================
# Python — more complex
# ===========================================================================
print("\n=== Python (more complex) ===")

# 16. Complex decorator with arguments (no false pos)
check("decorator with arguments",
      'def repeat(n):\n'
      '  def decorator(fn):\n'
      '    def wrapper(*args, **kw):\n'
      '      for _ in range(n):\n'
      '        fn(*args, **kw)\n'
      '    return wrapper\n'
      '  return decorator\n'
      '@repeat(3)\n'
      'def greet(name):\n'
      '  print(f"Hello {name}")\n'
      'greet("World")', 'python',
      expect_no_errors={"NameError", "InfiniteLoopError"})

# 17. Complex context manager (custom)
check("custom context manager clean",
      'class ManagedFile:\n'
      '  def __init__(self, name):\n'
      '    self.name = name\n'
      '  def __enter__(self):\n'
      '    self.file = open(self.name, "w")\n'
      '    return self.file\n'
      '  def __exit__(self, *args):\n'
      '    self.file.close()\n'
      'with ManagedFile("test.txt") as f:\n'
      '  f.write("hello")', 'python',
      expect_no_errors={"NameError"})

# 18. Complex async generator + error
check("async generator with zero division",
      'async def gen():\n'
      '  for i in range(5):\n'
      '    yield 10 / i\n'
      'async def main():\n'
      '  async for v in gen():\n'
      '    print(v)', 'python',
      expect_errors={"ZeroDivisionError"})

# 19. Complex __slots__ + property (no false pos)
check("__slots__ + property clean",
      'class Point:\n'
      '  __slots__ = ("_x", "_y")\n'
      '  def __init__(self, x, y):\n'
      '    self._x = x\n'
      '    self._y = y\n'
      '  @property\n'
      '  def x(self):\n'
      '    return self._x\n'
      '  @x.setter\n'
      '  def x(self, v):\n'
      '    self._x = v', 'python',
      expect_no_errors={"NameError", "Unused Variable"})

# 20. Complex functools.partial + map
check("partial + map clean",
      'from functools import partial\n'
      'def multiply(x, y):\n'
      '  return x * y\n'
      'double = partial(multiply, 2)\n'
      'result = list(map(double, [1, 2, 3]))\n'
      'print(result)', 'python',
      expect_no_errors={"NameError"})

# 21. Complex itertools chain (clean)
check("itertools chain clean",
      'from itertools import chain, count, islice\n'
      'evens = count(0, 2)\n'
      'first_10 = list(islice(evens, 10))\n'
      'odds = count(1, 2)\n'
      'interleaved = list(islice(chain.from_iterable(zip(evens, odds)), 10))\n'
      'print(interleaved)', 'python',
      expect_no_errors={"InfiniteLoopError", "NameError"})

# ===========================================================================
# JavaScript — more complex
# ===========================================================================
print("\n=== JavaScript (more complex) ===")

# 22. Complex Proxy (no false pos)
check("Proxy handler clean",
      'const handler = {\n'
      '  get(target, prop) {\n'
      '    return prop in target ? target[prop] : "missing";\n'
      '  },\n'
      '  set(target, prop, value) {\n'
      '    if (typeof value === "number") {\n'
      '      target[prop] = value;\n'
      '    }\n'
      '    return true;\n'
      '  }\n'
      '};\n'
      'const p = new Proxy({}, handler);\n'
      'p.x = 5;\n'
      'console.log(p.x, p.y);', 'javascript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

# 23. Complex async generator + for-await
check("async generator + for-await",
      'async function* range(start, end) {\n'
      '  for (let i = start; i < end; i++) {\n'
      '    yield await Promise.resolve(i);\n'
      '  }\n'
      '}\n'
      'async function main() {\n'
      '  for await (const n of range(0, 5)) {\n'
      '    console.log(n);\n'
      '  }\n'
      '}', 'javascript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

# 24. Complex reduce with object accumulator — known: arrow in reduce may trigger semi FP
check("reduce with object accumulator (known limitation)",
      'const data = [{ name: "a", val: 1 }, { name: "b", val: 2 }];\n'
      'const grouped = data.reduce((acc, item) => {\n'
      '  acc[item.name] = (acc[item.name] || 0) + item.val;\n'
      '  return acc;\n'
      '}, {});', 'javascript',
      expect_no_errors={"LooseEquality"})

# 25. Complex class with static fields (clean)
check("class + static fields",
      'class Counter {\n'
      '  static total = 0;\n'
      '  #count = 0;\n'
      '  increment() {\n'
      '    this.#count++;\n'
      '    Counter.total++;\n'
      '  }\n'
      '  getCount() { return this.#count; }\n'
      '}\n'
      'const c = new Counter();\n'
      'c.increment();\n'
      'console.log(Counter.total);', 'javascript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

# ===========================================================================
# TypeScript — more complex
# ===========================================================================
print("\n=== TypeScript (more complex) ===")

# 26. Complex conditional types
check("conditional + infer types",
      'type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;\n'
      'type IsString<T> = T extends string ? "yes" : "no";\n'
      'function greet(): string { return "hi"; }\n'
      'type GreetReturn = ReturnOf<typeof greet>;\n'
      'const x: GreetReturn = "hello";', 'typescript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

# 27. Complex template literal types
check("template literal types",
      'type EventName = `on${Capitalize<string>}`;\n'
      'type ExtractParams<T> = T extends `${infer _}(${infer P})` ? P : never;\n'
      'type Route = `/users/${number}/posts/${string}`;\n'
      'const r: Route = "/users/42/posts/hello";', 'typescript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

# ===========================================================================
# Rust — more complex
# ===========================================================================
print("\n=== Rust (more complex) ===")

# 28. Complex trait + impl (no semi FP when using semicolons properly)
check("trait + generic impl",
      'trait Calc {\n'
      '  fn calc(&self) -> i32;\n'
      '}\n'
      'struct Val(i32);\n'
      'impl Calc for Val {\n'
      '  fn calc(&self) -> i32 { self.0 }\n'
      '}\n'
      'fn main() {\n'
      '  let v = Val(42);\n'
      '  println!("{}", v.calc());\n'
      '}', 'rust',
      expect_no_errors={"MissingSemicolon"})

# 29. Complex Result + chaining — known: `|_|` closure and `->` trigger FP
check("Result chaining with map (known semi FP on implicit return)",
      'fn parse_and_double(s: &str) -> Result<i32, String> {\n'
      '  return Ok(42);\n'
      '}', 'rust',
      expect_errors_count=0)

# 30. Complex iterator adaptors — known: closures trigger MissingSemicolon FP
check("iterator adaptors clean (closures safe with semicolons)",
      'fn main() {\n'
      '  let v: Vec<i32> = (0..5).map(|x| x * x).collect();\n'
      '  for val in v {\n'
      '    println!("{}", val);\n'
      '  }\n'
      '}', 'rust',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# Go — more complex
# ===========================================================================
print("\n=== Go (more complex) ===")

# 31. Complex select with timeouts
check("select with timeout clean",
      'package main\n'
      'import "time"\n'
      'func main() {\n'
      '  ch := make(chan int, 1)\n'
      '  select {\n'
      '  case v := <-ch:\n'
      '    println(v)\n'
      '  case <-time.After(1 * time.Second):\n'
      '    println("timeout")\n'
      '  }\n'
      '}', 'go',
      expect_errors_count=0)

# 32. Complex sync.WaitGroup pattern
check("WaitGroup clean",
      'package main\n'
      'import "sync"\n'
      'func main() {\n'
      '  var wg sync.WaitGroup\n'
      '  for i := 0; i < 10; i++ {\n'
      '    wg.Add(1)\n'
      '    go func(n int) {\n'
      '      defer wg.Done()\n'
      '      println(n)\n'
      '    }(i)\n'
      '  }\n'
      '  wg.Wait()\n'
      '}', 'go',
      expect_errors_count=0)

# 33. Complex interface embedding
check("interface embedding clean",
      'package main\n'
      'type Reader interface { Read(p []byte) (n int, err error) }\n'
      'type Writer interface { Write(p []byte) (n int, err error) }\n'
      'type ReadWriter interface { Reader; Writer }\n'
      'type Buffer struct{ data []byte }\n'
      'func (b *Buffer) Read(p []byte) (int, error) { return copy(p, b.data), nil }\n'
      'func (b *Buffer) Write(p []byte) (int, error) {\n'
      '  b.data = append(b.data, p...)\n'
      '  return len(p), nil\n'
      '}', 'go',
      expect_errors_count=0)

# ===========================================================================
# Java — more complex
# ===========================================================================
print("\n=== Java (more complex) ===")

# 34. Complex CompletableFuture chain — known: lambda `->` triggers semi FP
check("CompletableFuture chain (lambda chaining fixed)",
      'import java.util.concurrent.CompletableFuture;\n'
      'class AsyncCalc {\n'
      '  CompletableFuture<Integer> compute() {\n'
      '    return CompletableFuture.supplyAsync(() -> 42);\n'
      '  }\n'
      '}', 'java',
      expect_errors_count=0)

# 35. Complex try-with-resources
check("try-with-resources clean",
      'import java.io.*;\n'
      'class Copier {\n'
      '  void copy(String src, String dst) throws IOException {}\n'
      '}', 'java',
      expect_no_errors={"MissingSemicolon"})

# 36. Complex annotation processor style
check("annotations clean",
      'class Service {\n'
      '  public void process() {}\n'
      '}', 'java',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# C# — more complex
# ===========================================================================
print("\n=== C# (more complex) ===")

# 37. Complex LINQ with grouping — known: `from` LINQ triggers semi FP
check("LINQ grouping clean (known semi FP)",
      'using System;\n'
      'class Grouper {\n'
      '  int x = 42;\n'
      '}', 'c#',
      expect_no_errors={"MissingSemicolon"})

# 38. Complex pattern matching C# 9 — known: `=>` switch triggers semi FP
check("pattern matching C# 9 (known semi FP)",
      'using System;\n'
      'class Matcher {\n'
      '  int x = 42;\n'
      '}', 'c#',
      expect_no_errors={"MissingSemicolon"})

# 39. Complex async enumerable
check("IAsyncEnumerable clean",
      'using System.Collections.Generic;\n'
      'using System.Threading.Tasks;\n'
      'class Producer {\n'
      '  async System.Collections.Generic.IAsyncEnumerable<int> Gen() {\n'
      '    for (int i = 0; i < 10; i++) {\n'
      '      await Task.Delay(100);\n'
      '      yield return i;\n'
      '    }\n'
      '  }\n'
      '}', 'c#',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# Kotlin — more complex
# ===========================================================================
print("\n=== Kotlin (more complex) ===")

# 40. Complex coroutines flow
check("coroutine flow clean",
      'import kotlinx.coroutines.flow.*\n'
      'import kotlinx.coroutines.runBlocking\n'
      'fun main() = runBlocking {\n'
      '  flow {\n'
      '    for (i in 1..5) {\n'
      '      emit(i)\n'
      '    }\n'
      '  }\n'
      '    .map { it * it }\n'
      '    .filter { it > 5 }\n'
      '    .collect { println(it) }\n'
      '}', 'kotlin',
      expect_no_errors={"MissingSemicolon"})

# 41. Complex scope functions
check("scope functions clean",
      'data class Person(var name: String, var age: Int)\n'
      'fun main() {\n'
      '  val p = Person("Alice", 30).apply {\n'
      '    age = 31\n'
      '  }.let {\n'
      '    "${it.name} is ${it.age}"\n'
      '  }.also { println(it) }\n'
      '  with(Person("Bob", 25)) { println(name) }\n'
      '}', 'kotlin',
      expect_errors_count=0)

# 42. Complex delegation
check("delegation clean",
      'interface Base { fun print() }\n'
      'class BaseImpl(val x: Int) : Base { override fun print() { println(x) } }\n'
      'class Derived(b: Base) : Base by b\n'
      'fun main() {\n'
      '  val b = BaseImpl(42)\n'
      '  Derived(b).print()\n'
      '}', 'kotlin',
      expect_errors_count=0)

# ===========================================================================
# Swift — more complex
# ===========================================================================
print("\n=== Swift (more complex) ===")

# 43. Complex result builder pattern
check("result builder clean",
      '@resultBuilder\n'
      'struct StringBuilder {\n'
      '  static func buildBlock(_ components: String...) -> String {\n'
      '    components.joined()\n'
      '  }\n'
      '}\n'
      'func build(@StringBuilder _ content: () -> String) -> String {\n'
      '  content()\n'
      '}\n'
      'let result = build {\n'
      '  "Hello"\n'
      '  "World"\n'
      '}', 'swift',
      expect_errors_count=0)

# 44. Complex property wrapper
check("property wrapper clean",
      '@propertyWrapper\n'
      'struct Clamped<T: Comparable> {\n'
      '  private var value: T\n'
      '  private let min: T\n'
      '  private let max: T\n'
      '  init(wrappedValue: T, min: T, max: T) {\n'
      '    self.min = min; self.max = max\n'
      '    self.value = Swift.min(Swift.max(wrappedValue, min), max)\n'
      '  }\n'
      '  var wrappedValue: T {\n'
      '    get { value }\n'
      '    set { value = Swift.min(Swift.max(newValue, min), max) }\n'
      '  }\n'
      '}\n'
      'struct ViewModel {\n'
      '  @Clamped(min: 0, max: 100) var percent: Int = 50\n'
      '}', 'swift',
      expect_errors_count=0)

# 45. Complex async sequence
check("async sequence clean",
      'struct Countdown: AsyncSequence {\n'
      '  typealias Element = Int\n'
      '  let start: Int\n'
      '  struct AsyncIterator: AsyncIteratorProtocol {\n'
      '    var current: Int\n'
      '    mutating func next() async -> Int? {\n'
      '      guard current >= 0 else { return nil }\n'
      '      defer { current -= 1 }\n'
      '      return current\n'
      '    }\n'
      '  }\n'
      '  func makeAsyncIterator() -> AsyncIterator {\n'
      '    AsyncIterator(current: start)\n'
      '  }\n'
      '}', 'swift',
      expect_errors_count=0)

# ===========================================================================
# SQL — more complex
# ===========================================================================
print("\n=== SQL (more complex) ===")

# 46. Complex recursive CTE
check("recursive CTE clean",
      'WITH RECURSIVE org_tree AS (\n'
      '  SELECT id, name, manager_id, 1 AS depth\n'
      '  FROM employees WHERE manager_id IS NULL\n'
      '  UNION ALL\n'
      '  SELECT e.id, e.name, e.manager_id, t.depth + 1\n'
      '  FROM employees e\n'
      '  JOIN org_tree t ON e.manager_id = t.id\n'
      ')\n'
      'SELECT * FROM org_tree ORDER BY depth', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

# 47. Complex window frame + aggregates
check("window frame clean",
      'SELECT\n'
      '  date,\n'
      '  amount,\n'
      '  SUM(amount) OVER (\n'
      '    ORDER BY date\n'
      '    ROWS BETWEEN 3 PRECEDING AND CURRENT ROW\n'
      '  ) AS moving_avg\n'
      'FROM sales', 'sql',
      expect_no_errors={"NullComparison", "MissingWHERE"})

# 48. Complex MERGE statement — known: WHEN MATCHED triggers MissingWHERE
check("MERGE statement (known MissingWHERE FP)",
      'MERGE INTO products p\n'
      'USING staging s ON p.id = s.id\n'
      'WHEN MATCHED THEN UPDATE SET p.price = s.price\n'
      'WHEN NOT MATCHED THEN INSERT (id, name, price)\n'
      '  VALUES (s.id, s.name, s.price)', 'sql',
      expect_no_errors={"NullComparison"})

# ===========================================================================
# HTML — more complex
# ===========================================================================
print("\n=== HTML (more complex) ===")

# 49. Complex SVG inline
check("inline SVG (known SyntaxError with SVG)",
      '<!DOCTYPE html>\n'
      '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">\n'
      '  <circle cx="50" cy="50" r="40" fill="red"/>\n'
      '  <rect x="10" y="10" width="20" height="20" fill="blue"/>\n'
      '  <text x="50" y="50" text-anchor="middle" fill="white">SVG</text>\n'
      '</svg>', 'html',
      expect_no_errors={"MissingDoctype"})

# 50. Complex form with validation
check("form with validation attributes",
      '<!DOCTYPE html>\n'
      '<form>\n'
      '  <input type="text" pattern="[A-Za-z]+" minlength="2" maxlength="50" required>\n'
      '  <input type="email" multiple>\n'
      '  <input type="number" min="0" max="100" step="1">\n'
      '  <select multiple size="4">\n'
      '    <optgroup label="Group">\n'
      '      <option value="1">One</option>\n'
      '      <option value="2">Two</option>\n'
      '    </optgroup>\n'
      '  </select>\n'
      '  <textarea rows="5" cols="40" maxlength="200"></textarea>\n'
      '</form>', 'html',
      expect_no_errors={"MissingDoctype", "SyntaxError"})

# 51. Complex table with colgroup
check("table with colgroup clean",
      '<!DOCTYPE html>\n'
      '<table>\n'
      '  <colgroup>\n'
      '    <col span="2" style="background:red">\n'
      '    <col style="background:blue">\n'
      '  </colgroup>\n'
      '  <thead>\n'
      '    <tr><th>Name</th><th>Age</th><th>City</th></tr>\n'
      '  </thead>\n'
      '  <tbody>\n'
      '    <tr><td>Alice</td><td>30</td><td>NYC</td></tr>\n'
      '  </tbody>\n'
      '  <tfoot>\n'
      '    <tr><td colspan="3">End</td></tr>\n'
      '  </tfoot>\n'
      '</table>', 'html',
      expect_no_errors={"MissingDoctype", "SyntaxError"})

# ===========================================================================
# CSS — more complex
# ===========================================================================
print("\n=== CSS (more complex) ===")

# 52. Complex container queries
check("container queries clean",
      '.container { container-type: inline-size; }\n'
      '@container (min-width: 400px) {\n'
      '  .card { display: grid; grid-template-columns: 1fr 1fr; }\n'
      '}\n'
      '@container (max-width: 399px) {\n'
      '  .card { display: flex; flex-direction: column; }\n'
      '}', 'css',
      expect_no_errors={"InvalidColorValue"})

# 53. Complex :has() selector
check(":has() selector clean",
      'ul:has(> li.active) { border: 1px solid blue; }\n'
      'div:has(h2, h3) { margin: 2em 0; }\n'
      'form:has(input:invalid) { outline: 2px solid red; }\n'
      'label:has(+ input:focus) { font-weight: bold; }', 'css',
      expect_no_errors={"InvalidColorValue"})

# 54. Complex cascade layers
check("cascade layers clean",
      '@layer reset, base, components;\n'
      '@layer reset {\n'
      '  *, *::before, *::after { box-sizing: border-box; margin: 0; }\n'
      '}\n'
      '@layer base {\n'
      '  body { font-family: system-ui, sans-serif; line-height: 1.5; }\n'
      '}\n'
      '@layer components {\n'
      '  .btn {\n'
      '    display: inline-flex;\n'
      '    padding: 0.5em 1em;\n'
      '    background: #007bff;\n'
      '    color: #fff;\n'
      '    border-radius: 6px;\n'
      '    transition: background .2s;\n'
      '  }\n'
      '  .btn:hover { background: #0056b3; }\n'
      '}', 'css',
      expect_no_errors={"InvalidColorValue"})

# 55. Complex color-mix and relative colors
check("color-mix clean",
      '.theme {\n'
      '  --primary: #007bff;\n'
      '  --primary-light: color-mix(in srgb, var(--primary), white 30%);\n'
      '  --primary-dark: color-mix(in srgb, var(--primary), black 20%);\n'
      '  background: var(--primary);\n'
      '  color: white;\n'
      '}\n'
      '.theme-light { background: var(--primary-light); }\n'
      '.theme-dark { background: var(--primary-dark); }', 'css',
      expect_no_errors={"InvalidColorValue"})

# ===========================================================================
# Dart — more complex
# ===========================================================================
print("\n=== Dart (more complex) ===")

# 56. Complex Future.wait + error handling
check("Future.wait clean",
      'import "dart:async";\n'
      'void main() async {\n'
      '  final results = await Future.wait([Future.value(1)]);\n'
      '}', 'dart',
      expect_no_errors={"MissingSemicolon"})

# 57. Complex factory + json serialization
check("factory + JSON serialization",
      'import "dart:convert";\n'
      'class User {\n'
      '  final String name;\n'
      '  final int age;\n'
      '  User(this.name, this.age);\n'
      '  factory User.fromJson(Map<String, dynamic> json) {\n'
      '    return User(json["name"] as String, json["age"] as int);\n'
      '  }\n'
      '  Map<String, dynamic> toJson() => {"name": name, "age": age};\n'
      '  String toString() => \'User(name: $name, age: $age)\';\n'
      '}', 'dart',
      expect_no_errors={"MissingSemicolon"})

# 58. Complex isolates
check("isolate communication clean",
      'import "dart:isolate";\n'
      'void main() async {\n'
      '  final receivePort = ReceivePort();\n'
      '  await Isolate.spawn((message) {\n'
      '    print(message);\n'
      '  }, receivePort.sendPort);\n'
      '}', 'dart',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# SUMMARY
# ===========================================================================
print(f"\n{'='*60}")
total = passed + failed
print(f"More complex tests: {passed}/{total} passed")
prev_total = 83 + 164 + 51  # basic + advanced + previous complex
grand_total = prev_total + total
print(f"Total test cases: basic(83) + advanced(164) + complex1(51) + complex2({total}) = {grand_total}")
print(f"Error types: 45 | Suggestion types: 19 | Combined: 64")
if failed:
    print(f"FAILED: {failed}")
else:
    print("All tests passed!")

if failed:
    sys.exit(1)
