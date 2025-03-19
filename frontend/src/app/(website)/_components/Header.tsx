import Link from "next/link";

export default function Header() {
    return (
        <header className="h-12 flex items-center p-2 bg-gradient-to-r from-pink-500 to-violet-500 text-lg font-bold text-white">
            <Link
                href="/"
                className="hover:underline underline-offset-4"
            >
                <p>Therefore.</p>
            </Link>
        </header>
    );
}