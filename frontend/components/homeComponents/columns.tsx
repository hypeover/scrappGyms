"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export type gymsData = {
  network: string;
  address: string;
  city: string;
  hours: Record<string, string>;
  link: string;
};

const DAYS_ORDER = [
  { key: "Monday", label: "Poniedziałek" },
  { key: "Tuesday", label: "Wtorek" },
  { key: "Wednesday", label: "Środa" },
  { key: "Thursday", label: "Czwartek" },
  { key: "Friday", label: "Piątek" },
  { key: "Saturday", label: "Sobota" },
  { key: "Sunday", label: "Niedziela" },
] as const;

const formatOpeningHours = (rawTime: string | undefined) => {
  if (!rawTime) return "Zamknięte";
  
  return rawTime
    .split('-')
    .map(time => {
      const parts = time.trim().split(':');
      const hours = parts[0].padStart(2, '0');
      const minutes = parts[1] ? parts[1].padStart(2, '0') : '00';
      
      return `${hours}:${minutes}`;
    })
    .join(' - '); 
};

export const columns: ColumnDef<gymsData>[] = [
  {
    accessorKey: "network",
    header: "Network",
    size: 180,
  },
  {
    accessorKey: "city",
    header: "City",
    size: 150,
  },
  {
    accessorKey: "address",
    header: "Address",
    size: 250,
  },
  {
    accessorKey: "link",
    header: "Link",
    size: 150,
    cell: ({ row }) => {
      const link = row.getValue("link") as string;
      return (
        <a className="font-medium" target="_blank" href={link}>
          Link to website
        </a>
      );
    },
  },
  {
    accessorKey: "hours",
    header: "Hours open",
    size: 140,
    cell: ({ row }) => {
      return (
        <div className="flex justify-center">
          <Dialog>
            <DialogTrigger asChild>
              <Button className="cursor-pointer rounded-xl " variant="outline">
                Hours
              </Button>
            </DialogTrigger>
            <DialogContent showCloseButton={false}>
              <DialogHeader>
                <DialogTitle>
                  <div className="flex flex-row space-x-2 text-lg -inset-y-50 ">
                    <p>{row.original.city}</p>
                    <p>{row.original.address}</p>
                  </div>
                </DialogTitle>
                <div className="text-black mt-2">
                  <ul className="space-y-1">
                    {DAYS_ORDER.map(({ key, label }) => {
                      const time = row.original.hours[key];
                      return (
                        <li
                          key={key}
                          className="flex justify-between font-sans text-lg py-1 border-b border-zinc-50"
                        >
                          <span className="">{label}</span>
                          <span className="tabular-nums ">
                            {formatOpeningHours(time)}
                          </span>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              </DialogHeader>
            </DialogContent>
          </Dialog>
        </div>
      );
    },
  },
];
