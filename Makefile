.PHONY: release check test doc clean

RUSTFLAGS := -C code-model=kernel -C codegen-units=1
export RUSTFLAGS

# Détection de l'OS 
ifeq ($(OS),Windows_NT)
	# Utilisation de llvm-strip fourni par Rust sur Windows
	STRIP  := $(shell rustup run stable rustc --print sysroot)/lib/rustlib/x86_64-pc-windows-msvc/bin/llvm-strip.exe
	BINARY := target/release/simeis-server.exe
else
	# Utilisation de la commande strip système sur Linux/macOS
	STRIP  := strip
	BINARY := target/release/simeis-server
endif

#Compile en mode release
release:
	cargo build --release
	$(STRIP) $(BINARY)

# Vérifie le code
check:
	cargo check
	cargo clippy

# Lance les tests
test:
	cargo test

# Compile le manuel
doc:
	typst compile doc/manual.typ

# Nettoie les binaires
clean:
	cargo clean
	-rm -f doc/manual.pdf
