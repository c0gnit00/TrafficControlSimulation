## TrafficControlSimulation Layout

Python UI and C++ backend are kept in separate folders so the Visual Studio project only builds C++ artifacts while Python stays as plain scripts.

```
TrafficControlSimulation/
  CPPBackend/     # Visual Studio C++ project (.sln/.vcxproj)
    include/      # public headers (traffic_core.h)
    src/          # simulation, routing, incidents, IO
  python_app/     # Python Tkinter UI (no VS project needed)
```

### Build the C++ backend

1) Open `CPPBackend/Backend.sln` in Visual Studio and build Release/x64 (produces `traffic_core.exe` under `CPPBackend/build` or the VS output dir).
2) Alternatively, from a dev shell:
   - `cmake -S CPPBackend -B CPPBackend/build`
   - `cmake --build CPPBackend/build --config Release`

### Run the Python UI

1) `cd python_app`
2) Ensure Python 3 + Tkinter are installed.
3) `python gui.py`

The UI searches for the backend binary in `python_app/build` and `../CPPBackend/build`. If you drop the exe next to `gui.py`, it will be picked up as well.

### Quick notes

- Do not add Python files to the Visual Studio C++ project; keep them in `python_app`.
- If you expose the backend via pybind11, place bindings in `CPPBackend/bindings` (create as needed) and build a `.pyd` module that Python can `import`.
- Source code for the C++ core lives under `CPPBackend/src` and headers under `CPPBackend/include` to keep the project tidy.

