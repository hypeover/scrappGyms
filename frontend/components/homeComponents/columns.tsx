"use client"

import { ColumnDef } from "@tanstack/react-table"

export type gymsData = {
  network: string;
  address: string;
  city: string;
  hours: Record<string, string>;
  link: string;
}

export const columns: ColumnDef<gymsData>[] = [
  {
    accessorKey: "network",
    header: "Network",
  },
  {
    accessorKey: "city",
    header: "City",
  },
  {
    accessorKey: "address",
    header: "Address",
  },
  {
    accessorKey: "link",
    header: "Link",
    cell: ({ row }) => {
        const link = row.getValue("link")
        return <a target="_blank" href={link}>Link to website</a>
    }
  },
  {
    accessorKey: "hours",
    header: "Hours open",
  },
]