# Cleanup Required - Remove Old Schema Files

## Files to Remove

These old "extensions" schema files should be deleted as they've been replaced:

```
schema/mpf-jl-extensions-v1.json          ← DELETE (replaced by mpf-v5.json)
python/jl_mpf_spec/schema/mpf-jl-extensions-v1.json   ← DELETE (replaced by mpf-v5.json)
python/jl_mpf_spec/schema/mpf-jl-extensions-v5.json   ← DELETE (replaced by mpf-v5.json)
```

## Why Remove

- These files contain the old "extensions" terminology that we removed from the standard
- The codebase now uses only `mpf-v5.json` in both locations
- Keeping them creates confusion and outdated references
- They are not referenced anywhere in the active code

## Active Schema Files (Keep)

```
schema/mpf-v5.json                        ✓ KEEP
python/jl_mpf_spec/schema/mpf-v5.json    ✓ KEEP
```

## How to Clean Up

### Option 1: Manual Deletion (VS Code)
1. Open Explorer
2. Navigate to `schema/` and `python/jl_mpf_spec/schema/`
3. Right-click each `mpf-jl-extensions-*.json` file
4. Select "Delete"

### Option 2: Command Line (PowerShell/Bash)
```powershell
# From repository root
Remove-Item schema/mpf-jl-extensions-v1.json
Remove-Item python/jl_mpf_spec/schema/mpf-jl-extensions-v1.json
Remove-Item python/jl_mpf_spec/schema/mpf-jl-extensions-v5.json
```

### Option 3: Git (if using version control)
```bash
git rm schema/mpf-jl-extensions-v1.json
git rm python/jl_mpf_spec/schema/mpf-jl-extensions-v1.json
git rm python/jl_mpf_spec/schema/mpf-jl-extensions-v5.json
git commit -m "Remove old extension-named schema files"
```

## Verification After Cleanup

After deleting, verify only clean files remain:

```bash
# Should only show mpf-v5.json files
find . -name "*.json" -path "*/schema/*" | grep mpf
```

Expected output:
```
./schema/mpf-v5.json
./python/jl_mpf_spec/schema/mpf-v5.json
```
