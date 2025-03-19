import type { Metadata } from "next";
import { Noto_Sans, Noto_Sans_Mono } from "next/font/google";
import "../styles/globals.css";

const notoSans = Noto_Sans({
    variable: "--font-noto-sans",
    subsets: ["latin"],
    weight: ["400", "700"],
});

const notoSansMono = Noto_Sans_Mono({
    variable: "--font-noto-sans-mono",
    subsets: ["latin"],
    weight: ["400"],
});

export const metadata: Metadata = {
    title: "Frontend",
    description: "The Frontend",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={`${notoSans.variable} ${notoSansMono.variable} font-sans antialiased`}>{children}</body>
        </html>
    );
}
