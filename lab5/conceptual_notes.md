#### Lab 5 - GPT Conceptual Notes
This is what interleaving means:
```scss
read(A)   (T1)
read(B)   (T2)
write(A)  (T1)
write(B)  (T2)
```

> Interleaving = executing operations of different transactions in overlapping order to increase performance and concurrency.

---
A schedule is **conflict serializable** if:
> You can reorder (by swapping non-conflicting ops) the interleaved schedule into some serial schedule that produces the same result.

#### Why does acyclicity of the precedence graph imply conflict serializability?
> Acyclic graph = no contradictory ordering constraints → serial order exists → conflict serializable.

---
#### How do conflicts add edges? 
Two operations conflict if:
1. Same item (e.g., A vs A),
2. Different transactions,
3. At least one is a write.

Examples:
* r1(A) / w5(A) → conflict
* w1(C) / r5(C) → conflict
* w1(C) / w5(C) → conflict

Not conflicts
* r1(A) / r5(A) → OK
* r1(A) / w5(B) → OK (different items)

#### How does a conflict imply an edge? 
Suppose:
* T1: write(C) happens earlier in the schedule
* T5: read(C) happens later

Because these two operations conflict, we are **not allowed** to swap them.

That means:
> T1 **must** appear before T5 in any equivalent serial schedule.

This creates a precedence constraint → therefore edge:
T1 → T5