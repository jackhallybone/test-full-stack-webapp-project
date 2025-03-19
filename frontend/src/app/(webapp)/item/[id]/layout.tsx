import ViewBar from './_components/ViewBar';

export default async function Layout({
    children,
    params
}: {
    children: React.ReactNode;
    params: Promise<{ id: string }>;
}) {
    const id = (await params).id

    return (
        <div className='bg-green-100'>
            <ViewBar id={id} />
            {children}
        </div>
    );
}