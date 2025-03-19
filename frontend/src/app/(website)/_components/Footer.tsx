import Link from "next/link";

export default function Footer() {
    return (
        <footer className="h-7 flex items-center p-2 bg-gradient-to-r from-pink-500 to-violet-500 text-sm font-bold text-white">
            <Link
                href="/"
                className="hover:underline underline-offset-4"
            >
                <p>Therefore.</p>
            </Link>
        </footer>
    );
}