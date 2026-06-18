# Toutes les cibles disponibles (évite les conflits avec des fichiers du même nom)
.PHONY: release check test doc clean

# Options de compilation Rust : optimisation noyau, pas de parallélisme
RUSTFLAGS := -C code-model=kernel -C codegen-units=1
export RUSTFLAGS

# Détecte l'OS pour choisir le bon outil de strip
ifeq ($(OS),Windows_NT)
	# Sur Windows : on utilise llvm-strip fourni par Rust
	STRIP  := $(shell rustup run stable rustc --print sysroot)/lib/rustlib/x86_64-pc-windows-msvc/bin/llvm-strip.exe
	BINARY := target/release/simeis-server.exe
else
	# Sur Linux/macOS : strip système suffit
	STRIP  := strip
	BINARY := target/release/simeis-server
endif

# Compile en release et supprime les symboles de debug pour alléger le binaire oui
release:
	cargo build --release
	$(STRIP) $(BINARY)

# Vérifie que ça compile + passe clippy (analyse statique)
check:
	cargo check
	cargo clippy

# Lance tous les tests unitaires
test:
	cargo test

# Génère le manuel PDF depuis le fichier Typst
doc:
	typst compile doc/manual.typ

# Supprime tous les fichiers compilés et le PDF
clean:
	cargo clean
	-rm -f doc/manual.pdf
