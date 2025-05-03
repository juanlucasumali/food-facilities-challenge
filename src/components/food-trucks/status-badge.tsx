import { Badge } from "@/components/ui/badge"

interface StatusBadgeProps {
  status: string
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "APPROVED":
        return "bg-green-500 hover:bg-green-600"
      case "REQUESTED":
        return "bg-blue-500 hover:bg-blue-600"
      case "EXPIRED":
        return "bg-red-500 hover:bg-red-600"
      case "SUSPEND":
        return "bg-yellow-500 hover:bg-yellow-600"
      case "ISSUED":
        return "bg-purple-500 hover:bg-purple-600"
      default:
        return "bg-gray-500 hover:bg-gray-600"
    }
  }

  return (
    <Badge className={`${getStatusColor(status)} text-white`}>
      {status}
    </Badge>
  )
} 