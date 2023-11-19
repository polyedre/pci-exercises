# Rebase vs Merge

Let's try to explain why the two branches `merged` and `rebased` differs.

Here is the diff of the two branches:

```diff
➜ pci-exercises (rebased) ✗ git diff merged..rebased

diff --git a/libvirt.pp b/libvirt.pp
index bd5eabe..c37b5ea 100644
--- a/libvirt.pp
+++ b/libvirt.pp
@@ -278,20 +278,14 @@ class nova::compute::libvirt (
     validate_legacy(String, 'validate_string', $libvirt_cpu_model)
     nova_config {
       'libvirt/cpu_model': value => $libvirt_cpu_model;
-      'libvirt/cpu_model_extra_flags': value => $libvirt_cpu_model_extra_flags;
     }
   } else {
     nova_config {
       'libvirt/cpu_model': ensure => absent;
-      'libvirt/cpu_model_extra_flags': ensure => absent;
     }
     if $libvirt_cpu_model {
       warning('$libvirt_cpu_model requires that $libvirt_cpu_mode => "custom" and will be ignored')
     }
-
-    if $libvirt_cpu_model_extra_flags {
-      warning('$libvirt_cpu_model_extra_flags requires that $libvirt_cpu_mode => "custom" and will be ignored')
-    }
   }
 
   if $libvirt_cpu_mode_real != 'none' {
```

## Initial context

The two branches `queens` and `stein` share their history up to commit A. The
content of the commits 'B' and 'F' on both branches is similar.

```sh
➜ pci-exercises (master) ✗ git log upstream/stein upstream/queens --graph --oneline
* 2624c16 (upstream/queens) F
* 5e3521b B
| * 1ff2641 (upstream/stein) G
| * cf24853 F
| * 3fcdfa0 E
| * cb8c71a D
| * 849ef26 C
| * 372c155 B
|/
* edc8ed7 A
* 308f3a2 Initial release
```

## Merging vs Rebasing

When merging stein on queens, git create a commit with the diff between the two branches. All the lines that are present on HEAD but not in the target branch are automatically added, and lines present in the target branch but not in HEAD are part of the diff. As a result, the branch `merged` contains the files of `stein`, without the lines that were removed on `stein` but not on `merged`.

When rebasing, git switches to the target branch (stein) and then *replays* the
commits of the current branch (queens). In our case, git replayed B and F on
commit 1ff2641. There was no difference with 'B' (same content and same
history), the commit 'B' of branch queens was skipped automatically. As a result, the branch `rebased` has the same history as `stein`.

## Conclusion

To conclude, the branches `merged` and `rebased` differs because the merge command keeps the lines of HEAD that are removed on the target branch.
