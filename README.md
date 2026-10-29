# CaseZero: Algorithmic Crime Investigation

**CaseZero** is an investigative detective game where every core gameplay mechanic is directly powered by a fundamental Data Structure or Algorithm (DSA), written in **Python 3.10+** using standard library components only (no pip installs).

---

## 🕵️ Data Structures & Mechanics

- **Custom HashMap (`dsa/hashmap.py`)**: Polynomial rolling hash (`djb2`), separate chaining, automatic resizing when load factor $\alpha > 0.75$, with live bucket and collision stats. Serves as the primary storage for suspect dossiers and clue records.
- **Suspect Graph (`dsa/graph.py`)**: Suspect relationship network with typed edges (`COLLEAGUE`, `BLACKMAIL`, `CONSPIRACY`, `DEBT`, `EQUIPMENT`). Features Breadth-First Search (BFS) for collusion chains ($O(V + E)$) and Connected Components for syndicate detection.
- **Set Theory Engine (`dsa/sets_engine.py`)**: Filters viable suspects via $\text{Viable} = (\text{Universe} \setminus \text{Eliminated}) \cap \bigcap C_i$. Detects planted forgeries when the intersection yields the empty set ($\emptyset$), triggering the contradiction siren.
- **Investigation Tree (`dsa/tree.py`)**: $N$-ary decision tree structuring crime scene leads. Features Pre-Order DFS ("Deep Dive") and Level-Order BFS ("Broad Survey") sequences.
- **Searching Algorithms (`dsa/search.py`)**:
  - `TimelineBinarySearch`: $O(\log N)$ logarithmic search across sorted chronological access logs with Low, Mid, and High pointer step traces.
  - `EvidenceTrie`: $O(L)$ prefix tree for instant autocomplete over traits, weapons, and notes.

---

## 🚀 How to Run

### Web GUI (Recommended)
Starts the local server on `http://127.0.0.1:8000` and automatically opens your default browser:
```powershell
python main.py
```
*(Requires Python 3.10+; uses only built-in `http.server`.)*

### Terminal / CLI Edition
```powershell
python casezero_cli.py
```

### Run All Unit Tests
```powershell
python -m unittest discover tests
```
*34 test suites verify HashMaps, Graphs, Sets, Trees, Searching, Cases, and 200 procedural seeds.*
