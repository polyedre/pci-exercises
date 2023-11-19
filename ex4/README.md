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

According to the git manual, when merging stein on queens, git replays the
changes made on stein from 'A', and will create a commit with the diff.

When rebasing, git switches to the target branch (stein) and then *replays* the
commits of the current branch (queens). In our case, git replayed B and F on
commit 1ff2641. There was no difference with 'B' (same content and same
history), the commit 'B' of branch queens was skipped automatically.

The diff can be explained **by the order on which commits were used** when
building the result history:

- When merging, the order of commits applied to the final filesystem is:

   1ff2641: G stein
   cf24853: F stein
   3fcdfa0: E stein
   cb8c71a: D stein
   849ef26: C stein
   372c155: B stein
   2624c16: F queen
   5e3521b: B queen
   edc8ed7: A common

  This means that commits C, D and E of stein were applied **after** 'F queen'.

- When rebasing, 'B queen' was applied after 'B stein', and 'F queen' after 'F stein':

   2624c16: F queen
   5e3521b: B queen
   1ff2641: G stein
   cf24853: F stein
   3fcdfa0: E stein
   cb8c71a: D stein
   849ef26: C stein
   372c155: B stein
   edc8ed7: A common
   
   This explains why the diff between `upstream/stein` and `rebased` is empty.

## Conclusion

My conclusion is that the two methods differs by the order in which the commits are applied.

Edit: After a small test, it seems that while I guessed that merging `queens` on `stein` would result in the same filesystem as the rebase, the commits from merging `queens` on `stein` and `stein` on `queens` have the same content. This invalidates my theory.

