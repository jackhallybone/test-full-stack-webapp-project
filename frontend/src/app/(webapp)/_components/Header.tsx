import Link from "next/link";
import Breadcrumb from "./_nav/Breadcrumb";


type HeaderProps = {
  tag: "dashboard" | "project" | "item";
  id?: string;
}

export default function Header({ tag, id }: HeaderProps) {
  return (
    <div className="mb-4 flex flex-row items-center gap-x-2 border-b py-4">
      <Link
        href="/dashboard"
        className="font-script text-brand-off-white dark:text-brand-off-black bg-brand-off-black dark:bg-brand-off-white cursor-pointer rounded px-2 py-1 text-xl"
      >
        Therefore
      </Link>
      {tag == "item" && (
        <>
          <div>[VIEW]</div>
          <p>view of</p>
          <Breadcrumb tag={tag} id={id} />
        </>
      )}
    </div>
  );
}
