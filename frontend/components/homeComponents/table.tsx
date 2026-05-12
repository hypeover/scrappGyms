"use client";

import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getPaginationRowModel,
  ColumnFiltersState,
  getFilteredRowModel,
} from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import React from "react";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export function DataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    [],
  );
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onColumnFiltersChange: setColumnFilters,
    getFilteredRowModel: getFilteredRowModel(),
    state: {
      columnFilters,
    },
  });

  return (
    <div className="w-full mb-20">
      <div className="flex flex-row justify-between" >
        <div className="flex items-center py-4">
          <Input
            placeholder="Filter cities..."
            value={(table.getColumn("city")?.getFilterValue() as string) ?? ""}
            onChange={(event) =>
              table.getColumn("city")?.setFilterValue(event.target.value)
            }
            className="max-w-sm rounded-xl"
          />
        </div>
        <div className="flex items-center justify-end space-x-2 py-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
            className="rounded-xl"
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
            className="rounded-xl"
          >
            Next
          </Button>
        </div>
      </div>
      <div className="w-auto overflow-hidden rounded-xl w-full">
        <Table className="text-base min-h-[650px]\" >
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow className="border-0" key={headerGroup.id}>
                {headerGroup.headers.map((header, index) => {
                  const getColumnWidth = (columnId: string) => {
                    if (columnId === 'network') return '12%';
                    if (columnId === 'city') return '18%';
                    if (columnId === 'address') return '50%';
                    if (columnId === 'link') return '12%';
                    if (columnId === 'hours') return '8%';
                    return undefined;
                  };
                  return (
                    <TableHead 
                      style={{
                        width: getColumnWidth(header.column.id),
                      }}
                      className={`border-none ${
                        index === 0 ? "rounded-l-lg" : ""
                      } ${
                        index === headerGroup.headers.length - 1 ? "rounded-r-lg" : ""
                      }`}
                      key={header.id}
                    >
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext(),
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                  className="border-0 "
                >
                  {row.getVisibleCells().map((cell, index) => {
                    const getColumnWidth = (columnId: string) => {
                      if (columnId === 'network') return '12%';
                      if (columnId === 'city') return '18%';
                      if (columnId === 'address') return '50%';
                      if (columnId === 'link') return '12%';
                      if (columnId === 'hours') return '8%';
                      return undefined;
                    };
                    return (
                    <TableCell 
                      style={{
                        width: getColumnWidth(cell.column.id),
                      }}
                      key={cell.id}
                      className={`${
                        index === 0 ? "rounded-l-lg" : ""
                      } ${
                        index === row.getVisibleCells().length - 1 ? "rounded-r-lg" : ""
                      }`}
                    >
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext(),
                      )}
                    </TableCell>
                    );
                  })}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
