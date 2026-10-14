---
title: Figure pipeline test, erroring cells
short_title: Error test
description: Throwaway page for issue #77, testing what the build does when a cell raises.
kernelspec:
  name: python3
  display_name: Python 3
---

Throwaway test page for issue #77. The first cell raises and is tagged
`raises-exception`; the second is tagged `skip-execution`.

```{code-cell} python
:tags: [raises-exception]
1 / 0
```

```{code-cell} python
:tags: [skip-execution]
raise RuntimeError("this cell is never run")
```

```{code-cell} python
print("cell after the error ran")
```
