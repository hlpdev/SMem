# SMem
<img src="https://img.shields.io/github/v/release/hlpdev/SMem" alt=""> <img src="https://img.shields.io/badge/3.6-%2330648e?label=python
" alt="">

The SMem library is used to handle **interprocess communication** ***(IPC)*** 
platform independently in Python.

## Usage
> [!NOTE]
> You must provide a name for the shared memory instance.
> 
> The size of the shared memory defaults to 1024
> 
> The create flag on the shared memory instance defaults to false, 
> so make sure you ensure that an instance of the shared memory exists!

#### Creating a shared memory instance:
```python
from smem.smem import SMem

# Create the SMem instance with the "create" flag 
# enabled and a specified "size" of 1024
shared_memory = SMem("my_shared_memory", create=True, size=1024)
```

#### Attaching to a shared memory instance:
Useful for reading an existing shared memory instance.
```python
from smem.smem import SMem

# Create the SMem instance with the "size" flag set to 1024
# (the same as when we created it)
shared_memory = SMem("my_shared_memory", size=1024)
```

#### Writing to shared memory
Writing to shared memory will overwrite the existing value.
```python
# Assume "shared_memory" contains an active instance of SMem
data = b"This is my data to write!"
shared_memory.write(data)
```

#### Reading shared memory
```python
# Assume "shared_memory" contains an active instance of SMem
data = shared_memory.read()
```

#### Closing an instance
Closing an instance that created the shared memory file:
```python
# Assume "shared_memory" contains an active instance of SMem
# that created the shared memory file
shared_memory.close()
shared_memory.unlink()
```
Closing an instance that did not create the shared memory file:
```python
# Assume "shared_memory" contains an active instance of SMem
# that did not create the shared memory file
shared_memory.close()
```