import logging
from sqlalchemy.orm import Session
from backend.app.models.academic import Subject, Topic, LearningMaterial, Question
from backend.app.models.user import User
from backend.app.models.profile import StudentProfile
from backend.app.auth.security import get_password_hash

logger = logging.getLogger("edupulse.seed")

DEMO_EMAIL = "demo@edupulse.ai"
DEMO_PASSWORD = "Demo@1234"


def seed_demo_account_if_missing(db: Session):
    """Ensure a fixed demo account always exists, even after the free-tier
    database resets. Lets you demo the app with the same login every time
    instead of re-registering."""
    existing = db.query(User).filter(User.email == DEMO_EMAIL).first()
    if existing:
        return

    logger.info("Seeding demo account (%s)...", DEMO_EMAIL)
    demo_user = User(
        name="Demo Student",
        email=DEMO_EMAIL,
        password_hash=get_password_hash(DEMO_PASSWORD),
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    demo_profile = StudentProfile(
        user_id=demo_user.id,
        education_level="Undergraduate (B.Tech / BCA / B.Sc)",
        learning_goal="Semester Exam Preparation",
        preferred_difficulty="medium",
        daily_study_target=45,
        xp_points=50,
        streak_days=1,
    )
    db.add(demo_profile)
    db.commit()


def seed_database_if_empty(db: Session):
    """Seed comprehensive DBMS curriculum, learning materials, and practice questions."""
    seed_demo_account_if_missing(db)

    existing_subject = db.query(Subject).filter(Subject.name == "Database Management Systems (DBMS)").first()
    if existing_subject:
        return

    logger.info("Seeding DBMS subject, topics, learning materials, and questions...")

    dbms = Subject(
        name="Database Management Systems (DBMS)",
        description="Comprehensive undergraduate course covering relational database design, SQL querying, formal relational theory, normalization, ACID transactions, and disk indexing techniques."
    )
    db.add(dbms)
    db.commit()
    db.refresh(dbms)

    topics_data = [
        {
            "name": "Database Fundamentals",
            "description": "DBMS architecture, 3-tier schema, data independence, instances vs schemas, data models.",
            "difficulty": "easy",
            "order_index": 1,
            "materials": [
                {
                    "title": "Introduction to DBMS & Three-Schema Architecture",
                    "description": "Understand physical, logical, and external schemas with data independence principles.",
                    "material_type": "concept_notes",
                    "difficulty": "easy",
                    "content": """# Database Management Systems: Core Foundations

A **Database Management System (DBMS)** is specialized software that enables efficient storage, retrieval, manipulation, and administration of structured data.

---

### The Three-Schema Architecture (ANSI/SPARC)

To decouple user applications from physical storage structures, modern DBMS architectures employ three distinct levels of abstraction:

1. **External Level (View Schema)**:
   - Describes how individual end-users or application roles perceive the data.
   - Tailored views hide confidential columns and simplify complex tables.

2. **Conceptual Level (Logical Schema)**:
   - Defines the global logical structure of the entire database.
   - Encompasses entities, attributes, relationships, security constraints, and semantic rules.
   - Independent of underlying physical storage media.

3. **Internal Level (Physical Schema)**:
   - Dictates how bytes and records are physically allocated on persistent storage (disks, SSDs).
   - Involves B+ Trees, hashing algorithms, record pointers, clustering, and data compression.

---

### Data Independence: The Superpower of Abstraction

- **Logical Data Independence**: The capacity to alter the conceptual schema (e.g., adding an optional column or splitting a table) without necessitating changes to existing external views or client programs.
- **Physical Data Independence**: The capacity to modify physical storage details (e.g., reorganizing disk clusters or building an auxiliary index) without altering conceptual or external schemas.
"""
                }
            ],
            "questions": [
                {
                    "question": "Which level of the ANSI/SPARC Three-Schema Architecture defines how data is physically stored on disk blocks?",
                    "option_a": "Conceptual Level",
                    "option_b": "External Level",
                    "option_c": "Internal / Physical Level",
                    "option_d": "View Level",
                    "correct_answer": "C",
                    "explanation": "The Internal (Physical) schema specifies the physical storage structures, record layouts, indexing, and compression methods.",
                    "difficulty": "easy"
                },
                {
                    "question": "What is the primary definition of 'Physical Data Independence' in a DBMS?",
                    "option_a": "Modifying application code without changing user views",
                    "option_b": "Altering internal storage structures without modifying conceptual schemas",
                    "option_c": "Changing conceptual entity definitions without altering physical files",
                    "option_d": "Executing concurrent read queries without table locks",
                    "correct_answer": "B",
                    "explanation": "Physical data independence allows DBAs to reindex, repartition, or reorganize physical storage without affecting logical schemas or user queries.",
                    "difficulty": "medium"
                },
                {
                    "question": "In database terminology, what is the critical distinction between a 'Schema' and an 'Instance'?",
                    "option_a": "A schema changes with every INSERT query, whereas an instance is static",
                    "option_b": "A schema is the blueprint design, whereas an instance is the actual data populated at a specific moment",
                    "option_c": "A schema represents disk partitions, whereas an instance represents memory RAM",
                    "option_d": "A schema is relational only, while instances are NoSQL only",
                    "correct_answer": "B",
                    "explanation": "The schema is the overall structural design (rarely changed), while an instance is the snapshot of data stored in the database at a specific instant.",
                    "difficulty": "easy"
                }
            ]
        },
        {
            "name": "ER Model",
            "description": "Entity-Relationship modeling, strong vs weak entities, cardinalities, generalization, specialization.",
            "difficulty": "medium",
            "order_index": 2,
            "materials": [
                {
                    "title": "Entity-Relationship (ER) Modeling & Constraints",
                    "description": "Entities, relationships, composite/multivalued attributes, and weak entities.",
                    "material_type": "concept_notes",
                    "difficulty": "medium",
                    "content": """# Entity-Relationship (ER) Modeling

The ER model provides a conceptual blueprint for representing real-world enterprises.

### Fundamental Elements
- **Entity**: A distinct real-world object (e.g., `Student`, `Course`).
- **Strong Entity**: Possesses a primary key formed exclusively from its own attributes.
- **Weak Entity**: Lacks a sufficient key on its own; depends upon an identifying parent entity via an identifying relationship. Its partial key is called a **discriminator** (represented by a dashed underline).
- **Multivalued Attribute**: Can hold multiple values for a single entity instance (e.g., `phone_numbers`), symbolized by a double oval.
- **Composite Attribute**: Subdivided into finer components (e.g., `Address` -> `Street`, `City`, `PostalCode`).

### Cardinality Ratios
- One-to-One ($1:1$)
- One-to-Many ($1:N$)
- Many-to-Many ($M:N$) - Requires a junction table when translated into relational tables.
"""
                }
            ],
            "questions": [
                {
                    "question": "How is a weak entity set identified in an Entity-Relationship (ER) diagram?",
                    "option_a": "Through its own candidate key exclusively",
                    "option_b": "By its discriminator (partial key) combined with the primary key of its identifying strong entity",
                    "option_c": "Via a surrogate auto-increment key only",
                    "option_d": "By foreign keys pointing to secondary indices",
                    "correct_answer": "B",
                    "explanation": "Weak entities cannot be uniquely identified by their attributes alone; their identity requires their discriminator plus the identifying parent entity's primary key.",
                    "difficulty": "medium"
                },
                {
                    "question": "In standard Chen ER notation, how are multivalued attributes visually represented?",
                    "option_a": "Dashed rectangle",
                    "option_b": "Double oval / ellipse",
                    "option_c": "Double diamond",
                    "option_d": "Underlined rectangle",
                    "correct_answer": "B",
                    "explanation": "Multivalued attributes are denoted by double concentric ovals in ER diagrams.",
                    "difficulty": "easy"
                },
                {
                    "question": "When converting an M:N (Many-to-Many) relationship between two entities into relational tables, what is required?",
                    "option_a": "Merging both entities into a single denormalized table",
                    "option_b": "Creating a third junction/bridge table containing foreign keys from both participating tables",
                    "option_c": "Adding a foreign key column to only one of the existing tables",
                    "option_d": "Using a single primary key with CSV text fields",
                    "correct_answer": "B",
                    "explanation": "Many-to-many relationships must be mapped into an associative/junction table composed of composite foreign keys referencing both participating entities.",
                    "difficulty": "medium"
                }
            ]
        },
        {
            "name": "SQL",
            "description": "DDL, DML, DCL, aggregations, GROUP BY, HAVING, subqueries, window functions.",
            "difficulty": "medium",
            "order_index": 3,
            "materials": [
                {
                    "title": "Mastering SQL: Queries, Filtering & Aggregations",
                    "description": "Core clauses, execution order, WHERE vs HAVING, and subqueries.",
                    "material_type": "concept_notes",
                    "difficulty": "medium",
                    "content": """# Structured Query Language (SQL)

SQL is the declarative language for relational database interaction.

### Logical Query Processing Order
Unlike procedural programming, SQL clauses execute in this specific sequence:
1. `FROM` & `JOIN` (determine source tables and join cartesian)
2. `WHERE` (filter individual rows before grouping)
3. `GROUP BY` (aggregate records into groups)
4. `HAVING` (filter grouped summary rows)
5. `SELECT` (evaluate expressions and projections)
6. `DISTINCT` (eliminate duplicates)
7. `ORDER BY` (sort output dataset)
8. `LIMIT` / `OFFSET` (paging)

### Key Rule: WHERE vs HAVING
- `WHERE` filters rows *before* aggregation occurs; aggregate functions like `COUNT()` or `AVG()` are **forbidden** in `WHERE`.
- `HAVING` filters results *after* `GROUP BY` aggregates have been calculated.
"""
                }
            ],
            "questions": [
                {
                    "question": "What is the fundamental functional difference between the WHERE and HAVING clauses in SQL?",
                    "option_a": "WHERE filters before grouping; HAVING filters aggregated groups after GROUP BY",
                    "option_b": "HAVING applies to columns, while WHERE applies to rows only",
                    "option_c": "WHERE requires aggregate functions like AVG(), while HAVING does not",
                    "option_d": "HAVING executes before FROM and WHERE clauses",
                    "correct_answer": "A",
                    "explanation": "WHERE filters individual base tuples before grouping. HAVING filters groups produced by GROUP BY, allowing aggregate expressions.",
                    "difficulty": "medium"
                },
                {
                    "question": "Which SQL statement is classified as a Data Definition Language (DDL) command?",
                    "option_a": "UPDATE",
                    "option_b": "TRUNCATE",
                    "option_c": "INSERT",
                    "option_d": "SELECT",
                    "correct_answer": "B",
                    "explanation": "TRUNCATE is a DDL command because it deallocates the table's data pages directly in schema catalogs, unlike DELETE which is DML.",
                    "difficulty": "medium"
                },
                {
                    "question": "What does a query with `SELECT COUNT(*)` return if the table is completely empty?",
                    "option_a": "NULL",
                    "option_b": "0",
                    "option_c": "Runtime SQL error",
                    "option_d": "Empty set (no rows)",
                    "correct_answer": "B",
                    "explanation": "COUNT(*) on an empty table produces a single row containing the integer 0.",
                    "difficulty": "easy"
                }
            ]
        },
        {
            "name": "Joins",
            "description": "INNER, LEFT OUTER, RIGHT OUTER, FULL OUTER, CROSS, SELF joins, and join algorithms.",
            "difficulty": "medium",
            "order_index": 4,
            "materials": [
                {
                    "title": "Relational Joins & Execution Mechanics",
                    "description": "Understanding relational join semantics and NULL handling.",
                    "material_type": "concept_notes",
                    "difficulty": "medium",
                    "content": """# Relational Joins Explained

Joins combine records from two or more tables based on a related attribute.

### Types of Joins
- **INNER JOIN**: Returns rows only when there is a matching key in both tables.
- **LEFT (OUTER) JOIN**: Returns all rows from the left table; unmatched right-side attributes are filled with `NULL`.
- **RIGHT (OUTER) JOIN**: Returns all rows from the right table; unmatched left-side attributes are filled with `NULL`.
- **FULL (OUTER) JOIN**: Returns records when there is a match in either table; preserves unmatched rows from both sides.
- **CROSS JOIN**: Produces the Cartesian product ($|R| \\times |S|$ rows).
- **SELF JOIN**: A table joined to itself (e.g., an `Employees` table with an `employee_id` and `manager_id`).
"""
                }
            ],
            "questions": [
                {
                    "question": "If Table A contains 10 rows and Table B contains 5 rows, what is the exact number of rows produced by a CROSS JOIN?",
                    "option_a": "15 rows",
                    "option_b": "50 rows",
                    "option_c": "10 rows",
                    "option_d": "5 rows",
                    "correct_answer": "B",
                    "explanation": "A CROSS JOIN yields the Cartesian product: 10 * 5 = 50 rows.",
                    "difficulty": "easy"
                },
                {
                    "question": "When executing a LEFT OUTER JOIN, what values populate the columns of the right table when no matching key exists?",
                    "option_a": "0 or empty string",
                    "option_b": "NULL",
                    "option_c": "Default primary key",
                    "option_d": "The row is omitted entirely",
                    "correct_answer": "B",
                    "explanation": "In a LEFT JOIN, unmatched rows from the left table retain their values, and all columns from the non-matching right table evaluate to NULL.",
                    "difficulty": "easy"
                },
                {
                    "question": "How can a query find all records in Table A that have NO matching record in Table B using a JOIN?",
                    "option_a": "INNER JOIN on A.id = B.a_id",
                    "option_b": "LEFT JOIN on A.id = B.a_id WHERE B.a_id IS NULL",
                    "option_c": "CROSS JOIN WHERE A.id <> B.a_id",
                    "option_d": "NATURAL JOIN with DISTINCT",
                    "correct_answer": "B",
                    "explanation": "The anti-join pattern performs a LEFT JOIN and filters for rows where the right table's key IS NULL.",
                    "difficulty": "hard"
                }
            ]
        },
        {
            "name": "Functional Dependencies",
            "description": "Functional dependencies, Armstrong's Axioms, closure of attribute sets, minimal cover.",
            "difficulty": "hard",
            "order_index": 5,
            "materials": [
                {
                    "title": "Formal Functional Dependencies & Armstrong's Axioms",
                    "description": "Mathematical formulation of dependencies, closures, and candidate key derivation.",
                    "material_type": "concept_notes",
                    "difficulty": "hard",
                    "content": """# Functional Dependencies (FDs)

A Functional Dependency $X \\to Y$ over relation $R$ specifies that whenever two tuples agree on attribute set $X$, they must also agree on attribute set $Y$:
$$t_1[X] = t_2[X] \\implies t_1[Y] = t_2[Y]$$

---

### Armstrong's Axioms (Sound and Complete)

1. **Reflexivity Rule**:
   $$\\text{If } Y \\subseteq X, \\text{ then } X \\to Y$$
   *(e.g., {A, B} -> A is trivial)*

2. **Augmentation Rule**:
   $$\\text{If } X \\to Y, \\text{ then } XZ \\to YZ \\text{ for any } Z$$

3. **Transitivity Rule**:
   $$\\text{If } X \\to Y \\text{ and } Y \\to Z, \\text{ then } X \\to Z$$

### Secondary Derived Rules
- **Union Rule**: If $X \\to Y$ and $X \\to Z$, then $X \\to YZ$
- **Decomposition Rule**: If $X \\to YZ$, then $X \\to Y$ and $X \\to Z$
- **Pseudotransitivity**: If $X \\to Y$ and $WY \\to Z$, then $WX \\to Z$

### Attribute Closure $X^+$
The closure $X^+$ with respect to FD set $F$ is the set of all attributes functionally determined by $X$.
If $X^+$ contains all attributes of relation $R$, then $X$ is a **Superkey**. If no proper subset of $X$ is a superkey, $X$ is a **Candidate Key**.
"""
                }
            ],
            "questions": [
                {
                    "question": "Given relation R(A, B, C, D) with FDs: {A -> B, B -> C, C -> D}. What is the attribute closure of A, denoted as A+?",
                    "option_a": "{A}",
                    "option_b": "{A, B}",
                    "option_c": "{A, B, C, D}",
                    "option_d": "{B, C, D}",
                    "correct_answer": "C",
                    "explanation": "A -> B gives {A,B}. B -> C gives {A,B,C}. C -> D gives {A,B,C,D}. Therefore, A+ = {A,B,C,D}, making A a candidate key.",
                    "difficulty": "medium"
                },
                {
                    "question": "Which of Armstrong's Axioms states: 'If X -> Y and Y -> Z, then X -> Z'?",
                    "option_a": "Augmentation",
                    "option_b": "Reflexivity",
                    "option_c": "Transitivity",
                    "option_d": "Decomposition",
                    "correct_answer": "C",
                    "explanation": "The Transitivity rule states that if X determines Y and Y determines Z, then X determines Z.",
                    "difficulty": "easy"
                },
                {
                    "question": "Under which condition is a functional dependency X -> Y classified as trivial?",
                    "option_a": "When X is a candidate key",
                    "option_b": "When Y is a subset of X (Y ⊆ X)",
                    "option_c": "When X and Y have no intersecting attributes",
                    "option_d": "When Y has only integer values",
                    "correct_answer": "B",
                    "explanation": "An FD X -> Y is trivial if and only if the right-hand side attribute set Y is a subset of the left-hand side attribute set X.",
                    "difficulty": "medium"
                }
            ]
        },
        {
            "name": "Normalization",
            "description": "Anomalies, 1NF, 2NF, 3NF, BCNF, lossless join decomposition, dependency preservation.",
            "difficulty": "hard",
            "order_index": 6,
            "materials": [
                {
                    "title": "Relational Database Normalization (1NF to BCNF)",
                    "description": "Comprehensive guide to eliminating update, insertion, and deletion anomalies.",
                    "material_type": "concept_notes",
                    "difficulty": "hard",
                    "content": """# Database Normalization

Normalization decomposes relations to eliminate data redundancy and anomalies while preserving information.

---

### The Normal Forms Hierarchy
$$1\\text{NF} \\subset 2\\text{NF} \\subset 3\\text{NF} \\subset \\text{BCNF} \\subset 4\\text{NF} \\subset 5\\text{NF}$$

#### 1. First Normal Form (1NF)
- Each column must contain atomic (indivisible) values.
- No repeating groups or arrays stored in a single field.

#### 2. Second Normal Form (2NF)
- Must be in 1NF.
- **No Partial Dependency**: Every non-prime attribute must be fully functionally dependent on the primary key (no non-prime attribute can depend on a proper subset of any candidate key).

#### 3. Third Normal Form (3NF)
- Must be in 2NF.
- **No Transitive Dependency**: For every non-trivial FD $X \\to Y$:
  - Either $X$ is a **Superkey**, OR
  - $Y$ is a **Prime Attribute** (part of some candidate key).

#### 4. Boyce-Codd Normal Form (BCNF)
- A strictly stricter version of 3NF.
- For EVERY non-trivial FD $X \\to Y$, $X$ **MUST be a Superkey**.
- Guarantees zero redundancy from functional dependencies, but does not always guarantee dependency preservation.
"""
                }
            ],
            "questions": [
                {
                    "question": "A relation R(A, B, C) has candidate key AB. Which functional dependency would directly violate 2NF?",
                    "option_a": "AB -> C",
                    "option_b": "A -> C",
                    "option_c": "C -> A",
                    "option_d": "AB -> A",
                    "correct_answer": "B",
                    "explanation": "A is a proper subset of candidate key AB. A -> C makes non-prime attribute C partially dependent on key AB, violating 2NF.",
                    "difficulty": "hard"
                },
                {
                    "question": "What is the key difference between 3NF and BCNF requirements for an FD X -> Y?",
                    "option_a": "In 3NF, Y can be a prime attribute if X is not a superkey; in BCNF, X must strictly be a superkey",
                    "option_b": "BCNF permits multi-valued attributes while 3NF does not",
                    "option_c": "3NF requires B+ Tree indices on foreign keys",
                    "option_d": "BCNF guarantees dependency preservation in all decompositions",
                    "correct_answer": "A",
                    "explanation": "3NF relaxes the condition by allowing Y to be a prime attribute when X is not a superkey. BCNF strictly demands that X must be a superkey for every non-trivial FD.",
                    "difficulty": "hard"
                },
                {
                    "question": "What kind of dependency exists when non-prime attribute A determines non-prime attribute B via primary key K (K -> A and A -> B)?",
                    "option_a": "Partial Dependency",
                    "option_b": "Transitive Dependency",
                    "option_c": "Trivial Dependency",
                    "option_d": "Multivalued Dependency",
                    "correct_answer": "B",
                    "explanation": "A transitive dependency occurs when a non-key attribute depends on another non-key attribute rather than directly on the primary key.",
                    "difficulty": "medium"
                }
            ]
        },
        {
            "name": "Transactions",
            "description": "ACID properties, serializability, conflict serializability, precedence graphs, two-phase locking (2PL).",
            "difficulty": "hard",
            "order_index": 7,
            "materials": [
                {
                    "title": "Transactions & Concurrency Control (ACID & 2PL)",
                    "description": "ACID guarantees, conflict serializability, precedence graph cycle testing, and lock protocols.",
                    "material_type": "concept_notes",
                    "difficulty": "hard",
                    "content": """# Database Transactions & ACID Guarantees

A transaction is a logical unit of database work containing one or more SQL operations.

---

### The ACID Properties

1. **Atomicity (All-or-Nothing)**:
   - Either all operations of the transaction commit successfully, or the transaction is completely rolled back to its initial state.
   - Handled via WAL (Write-Ahead Logging) and undo logs.

2. **Consistency**:
   - The database transitions from one valid state to another valid state, preserving all integrity constraints, foreign keys, and invariants.

3. **Isolation**:
   - Concurrent executions of transactions produce the same state as if they were executed serially without overlap.
   - ANSI SQL Isolation Levels: *Read Uncommitted, Read Committed, Repeatable Read, Serializable*.

4. **Durability**:
   - Once a transaction commits, its modifications are permanently recorded on persistent storage and survive any power failure or system crash.

---

### Conflict Serializability & Precedence Graphs

Two operations in a concurrent schedule conflict if:
1. They belong to different transactions.
2. They access the exact same data item.
3. At least one of the operations is a **WRITE**.

A schedule is **conflict serializable** if and only if its precedence (serialization) graph contains **NO CYCLES**.
"""
                }
            ],
            "questions": [
                {
                    "question": "Which ACID property guarantees that committed transaction changes survive an abrupt system crash or hardware failure?",
                    "option_a": "Atomicity",
                    "option_b": "Consistency",
                    "option_c": "Isolation",
                    "option_d": "Durability",
                    "correct_answer": "D",
                    "explanation": "Durability ensures that once a transaction has committed, its updates persist in non-volatile storage even during hardware or operating system crashes.",
                    "difficulty": "easy"
                },
                {
                    "question": "In concurrency control, two operations conflict if and only if they meet which criteria?",
                    "option_a": "Different transactions, different data items, and both are reads",
                    "option_b": "Different transactions, same data item, and at least one is a write",
                    "option_c": "Same transaction, same data item, both writes",
                    "option_d": "Different transactions on separate physical disk blocks",
                    "correct_answer": "B",
                    "explanation": "A conflict requires distinct transactions accessing the identical item where at least one operation is a write (Read-Write, Write-Read, Write-Write).",
                    "difficulty": "medium"
                },
                {
                    "question": "What mathematical structure determines whether a concurrent schedule is conflict serializable?",
                    "option_a": "If its precedence graph is a Directed Acyclic Graph (contains no directed cycles)",
                    "option_b": "If the total number of reads equals total writes",
                    "option_c": "If all transactions acquire exclusive locks simultaneously",
                    "option_d": "If the binary search tree has height O(log N)",
                    "correct_answer": "A",
                    "explanation": "A schedule is conflict serializable if and only if its precedence graph contains no directed cycles (DAG).",
                    "difficulty": "hard"
                }
            ]
        },
        {
            "name": "Indexing",
            "description": "B-Trees, B+ Trees, clustered vs non-clustered indexes, hashing, index scan vs table scan.",
            "difficulty": "medium",
            "order_index": 8,
            "materials": [
                {
                    "title": "Database Storage & B+ Tree Indexing",
                    "description": "B+ Tree structure, why databases prefer B+ Trees over binary search trees, and clustered indexing.",
                    "material_type": "concept_notes",
                    "difficulty": "medium",
                    "content": """# Database Indexing & B+ Trees

An index is an auxiliary data structure that dramatically speeds up tuple retrieval at the cost of slower writes and extra storage.

---

### Why B+ Trees in Relational Databases?

- **High Fanout & Low Tree Depth**: A B+ Tree node matches the disk block size (typically 4KB–16KB) and can store hundreds of child pointers. Even a database with millions of rows has a tree height of only 3 or 4, requiring minimal disk I/O.
- **All Data in Leaf Nodes**: Internal nodes hold only search keys and child pointers, maximizing fanout.
- **Linked Leaf Level**: All leaf nodes are linked sequentially via a doubly-linked list, enabling extremely fast **range queries** (`WHERE age BETWEEN 20 AND 30`) without backtracking up the tree.

---

### Clustered vs Non-Clustered Indexes

- **Clustered Index**:
  - The physical order of table rows on disk matches the index key order.
  - A table can have **only ONE** clustered index (usually the primary key).
  - Leaf nodes contain the actual data rows.

- **Non-Clustered (Secondary) Index**:
  - Distinct from the physical storage arrangement.
  - Leaf nodes contain the indexed key and a pointer (RID or primary key value) to the actual row.
  - A table can have multiple non-clustered indexes.
"""
                }
            ],
            "questions": [
                {
                    "question": "Why do relational database engines prefer B+ Trees over standard Binary Search Trees (BST) for disk-based indexing?",
                    "option_a": "B+ Trees have lower fanout and use more memory",
                    "option_b": "B+ Trees have high fanout matching disk block sizes, keeping tree height extremely low to minimize disk I/O",
                    "option_b_alt": "B+ Trees do not require disk space",
                    "option_c": "BST trees do not support alphanumeric text strings",
                    "option_d": "B+ Trees automatically disable write locks",
                    "correct_answer": "B",
                    "explanation": "B+ Trees are wide and shallow with high fanout matching disk block size, minimizing expensive disk head movements/block reads.",
                    "difficulty": "medium"
                },
                {
                    "question": "What enables B+ Trees to execute range scans (e.g. BETWEEN 10 AND 50) with exceptional efficiency?",
                    "option_a": "All records are duplicated across every internal node",
                    "option_b": "The leaf nodes form a sequential doubly-linked list",
                    "option_c": "Binary search on memory registers",
                    "option_d": "Hash table buckets allocated at root",
                    "correct_answer": "B",
                    "explanation": "In a B+ Tree, all data resides in the leaf nodes, which are connected by pointers in a doubly-linked list, allowing fast sequential scanning across ranges.",
                    "difficulty": "medium"
                },
                {
                    "question": "How many Clustered Indexes can a single database table have?",
                    "option_a": "Exactly one, because physical disk rows can only be ordered in one way",
                    "option_b": "Up to 16 clustered indexes",
                    "option_c": "As many as there are foreign keys",
                    "option_d": "Unlimited, matching candidate keys",
                    "correct_answer": "A",
                    "explanation": "Because a clustered index determines the physical sequence of data records on disk, only one clustered index can exist per table.",
                    "difficulty": "easy"
                }
            ]
        }
    ]

    for t_data in topics_data:
        topic = Topic(
            subject_id=dbms.id,
            name=t_data["name"],
            description=t_data["description"],
            difficulty=t_data["difficulty"],
            order_index=t_data["order_index"]
        )
        db.add(topic)
        db.commit()
        db.refresh(topic)

        # Add learning materials
        for mat in t_data.get("materials", []):
            lm = LearningMaterial(
                topic_id=topic.id,
                title=mat["title"],
                description=mat["description"],
                content=mat["content"],
                material_type=mat["material_type"],
                difficulty=mat["difficulty"]
            )
            db.add(lm)

        # Add questions
        for q in t_data.get("questions", []):
            question = Question(
                topic_id=topic.id,
                question=q["question"],
                option_a=q["option_a"],
                option_b=q["option_b"],
                option_c=q["option_c"],
                option_d=q["option_d"],
                correct_answer=q["correct_answer"],
                explanation=q["explanation"],
                difficulty=q["difficulty"]
            )
            db.add(question)

    db.commit()
    logger.info("Successfully seeded DBMS topics, materials, and comprehensive questions!")
