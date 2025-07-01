import Header from "../../_components/Header";

export default async function ItemLayout({
  children,
  params
}: {
  children: React.ReactNode,
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return (
    <>
      <Header tag="item" id={id} />
      {children}
    </>
  );
}
