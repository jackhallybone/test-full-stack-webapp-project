import Header from "./_components/Header";
import Footer from "./_components/Footer";

export default function Layout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className='h-screen flex flex-col'>
            {/* <Notifications /> */}
            <div className="flex flex-col flex-1">
                <Header />
                <div className='flex-1 m-2'>
                    {children}
                </div>
                <Footer />
            </div>
        </div>
    );
}
