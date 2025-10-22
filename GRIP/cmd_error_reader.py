import subprocess, sys, re, datetime, json, ast
from pathlib import Path

PROJECT_DIR = r"C:\Users\pavit\programing\GRIP\GRIP"
LOG_FILE = "runtime_errors.json"

# ---------- STEP 1: Parse Traceback ----------
def parse_traceback(tb_text):
    trace_regex = r'File "(.+?)", line (\d+), in (.+?)'
    matches = re.findall(trace_regex, tb_text)
    error_match = re.search(r'([A-Za-z_]+(?:Error|Exception|DoesNotExist|Denied|Failed)): (.+)', tb_text.splitlines()[-1])

    frames = [{"file": f, "line": int(l), "function": fn} for f, l, fn in matches]
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "stack_frames": frames,
        "error_type": error_match.group(1) if error_match else "UnknownError",
        "error_message": error_match.group(2) if error_match else tb_text.splitlines()[-1],
    }

# ---------- STEP 2: Try to trace the origin ----------
def find_symbol_origin(file_path: str, line_num: int):
    """Finds likely symbol/function causing the error and traces where it was defined."""
    try:
        source = Path(file_path).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return None

    # Extract a few lines around the error line
    start = max(0, line_num - 5)
    end = min(len(source), line_num + 5)
    context = "\n".join(source[start:end])

    # Find possible symbol usage near the error line (e.g., NoteForm(...))
    m = re.search(r'([A-Z]\w+)\s*\(', context)
    if not m:
        return None
    symbol = m.group(1)

    # Look for import statement for that symbol
    imports = [l for l in source if f"import" in l and symbol in l]
    origin_file = None
    if imports:
        for imp in imports:
            if ".forms" in imp:
                origin_file = PROJECT_DIR + "\\core\\forms.py"
            elif ".models" in imp:
                origin_file = PROJECT_DIR + "\\core\\models.py"

    # If not found, fallback to forms.py (common pattern)
    if not origin_file:
        origin_file = PROJECT_DIR + "\\core\\forms.py"

    # Parse the target file to locate symbol definition
    try:
        target_path = Path(origin_file)
        text = target_path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name == symbol:
                return {
                    "symbol": symbol,
                    "defined_in": str(target_path),
                    "definition_line": node.lineno
                }
    except Exception:
        pass

    return {"symbol": symbol, "defined_in": "Unknown", "definition_line": None}

# ---------- STEP 3: Save structured error ----------
def save_error(err):
    path = Path(LOG_FILE)
    try:
        data = json.loads(path.read_text()) if path.exists() else []
    except json.JSONDecodeError:
        data = []
    data.append(err)
    path.write_text(json.dumps(data, indent=2))
    print(f"💾 Logged error in {LOG_FILE}")

# ---------- STEP 4: Run Django and capture live errors ----------
def run_and_capture_live():
    print(f"▶ Starting Django server log watcher...\n")

    process = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "8001"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr into stdout
        text=True,
        bufsize=1
    )

    buffer = []
    try:
        for line in iter(process.stdout.readline, ''):
            print(line, end="")  # live output
            buffer.append(line)

            # Detect end of a traceback block
            if re.search(r'([A-Za-z_]*Error|[A-Za-z_]*Exception|DoesNotExist|NotFound|Denied|Failed):', line):
                tb_text = "".join(buffer[-15:])  # capture last few lines
                err = parse_traceback(tb_text)

                # Add origin trace if it’s your project file
                if err["stack_frames"]:
                    last_user_frame = next((f for f in reversed(err["stack_frames"]) if "GRIP\\GRIP" in f["file"]), None)
                    if last_user_frame:
                        origin = find_symbol_origin(last_user_frame["file"], last_user_frame["line"])
                        if origin:
                            err["origin_trace"] = origin

                print("\n🧩 Parsed Error:")
                print(json.dumps(err, indent=2))
                save_error(err)
                buffer.clear()

    except KeyboardInterrupt:
        print("\n🛑 Stopping watcher manually...")
    finally:
        process.terminate()

# ---------- STEP 5: Entry ----------
if __name__ == "__main__":
    run_and_capture_live()
