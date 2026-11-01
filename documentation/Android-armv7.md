# Android 32-bit (armeabi-v7a) — experimental groundwork

Status: **unverified.** Nothing here has been compiled or run on a device. The
change only removes the places that forced `arm64-v8a`, so a CI run can show what
actually breaks in the engine on a 32-bit host.

## What changed

- `tools/native/android_abi.py` lists the supported ABIs and their toolchain triples.
- `apply_armv7_port.py` relaxes the engine's three `ports/android/*/CMakeLists.txt`
  ABI gates and retargets its Gradle `abiFilters` and staged-library directory.
- `stage_android_host.py`, `build_android_capstone.py` and `prepare_android_app.py`
  take `--abi` (default `arm64-v8a`, so existing builds are unchanged).
- `android_runtime.py` verifies ELF32 as well as ELF64 libraries.
- `android/rom_preparation.py` reads the compiler target from the preparation kit
  (`clang_target`), falling back to the previous AArch64 value.
- `.github/workflows/android-native-host-armv7.yml` builds the neutral host with
  NDK r29 for `armeabi-v7a` and stages it. Run it manually (workflow_dispatch).

## What is still missing

1. **The engine may not build or run on 32-bit.** Expect compile errors or
   pointer-width assumptions to surface in the first CI run.
2. **On-device ROM preparation has no armv7 toolchain.** Preparation compiles the
   translated game on the phone with a bundled compiler, Python, NumPy and Capstone,
   all arm64 today. The preparation-kit builder is not in this repository; it must
   emit armv7 binaries and a `clang_target` of `armv7a-linux-androideabi29`.
3. **NumPy for armeabi-v7a is not hash-pinned.** `prepare_android_app.py --abi
   armeabi-v7a` asks Chaquopy for `numpy==2.3.2`; whether that wheel exists for
   Python 3.13 on armeabi-v7a has not been checked.
4. **Performance is unknown.** The engine was measured at about 30 FPS on an
   Adreno 830. Low-end 32-bit devices (for example a Mali-G52 MP1) may be too slow
   and may lack the Vulkan features the renderer needs.

## Try it

In your fork, open Actions and run **Android native host prototype (armeabi-v7a,
experimental)**. To reproduce locally with NDK r29 and the pinned engine checked
out at `engine/`:

```sh
python tools/native/apply_android_port.py engine
python tools/native/apply_armv7_port.py engine
# then the remaining apply_* steps and the cmake/ninja commands from the workflow
python tools/native/stage_android_host.py --engine engine --build build/host \
  --ndk "$ANDROID_HOME/ndk/29.0.14206865" --abi armeabi-v7a --output out/host-armv7.tar.gz
```
