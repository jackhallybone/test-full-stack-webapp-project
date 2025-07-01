import { redirect } from 'next/navigation';

export default function ItemPage({ params }: { params: { id: string } }) {
  redirect(`/item/${params.id}/detail`);
}