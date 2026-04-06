"""Calculadora simple por línea de comandos."""


def calcular(a: float, op: str, b: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        return a / b
    raise ValueError(f"Operación no válida: {op}")


def main() -> None:
    print("Calculadora — operaciones: + - * /")
    print("Escribe 'salir' para terminar.")
    while True:
        entrada = input("> ").strip()
        if entrada.lower() in {"salir", "exit", "q"}:
            break
        try:
            partes = entrada.split()
            if len(partes) != 3:
                print("Formato: <num> <op> <num>  (ej: 2 + 3)")
                continue
            a, op, b = float(partes[0]), partes[1], float(partes[2])
            print(calcular(a, op, b))
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
