# 🌻 cli-decorator

small set of decorator functionallity for bash/python scripts

# 📦 installation

```bash
# force reinstall for development
python3 -m build && pip install dist/cli_decorator_{version}.whl --force-reinstall
```

# ⚙️ commands

Some commands are delivered to be able to use it in bash scripts

## cld

`echo` but with colors:

```bash
cld -c RED hello world

# you can also pipe into it
echo "hi" | cld -c BLUE
```

## cll

python `logging` in bash with some color and my personal taste:

```bash
cll -n TEST hello world

# same as cle you can pipe into it
ls | cll

# you can mix both
echo "hello!" | cld -c RED | cll -n SCRIPT
```

