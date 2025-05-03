import { useState } from "react"
import { DataTable } from "./components/food-trucks/data-table"
import { columns } from "./components/food-trucks/columns"
import { FoodTruck } from "./components/food-trucks/data-table"
import { searchByApplicant, searchByStreet, findNearbyTrucks } from "./lib/api"

function App() {
  const [data, setData] = useState<FoodTruck[]>([])
  const [searchType, setSearchType] = useState<"applicant" | "street" | "nearby">("nearby")
  const [searchQuery, setSearchQuery] = useState("")
  const [status, setStatus] = useState<string>("APPROVED")
  const [lat, setLat] = useState("")
  const [lng, setLng] = useState("")
  const [error, setError] = useState<string>("")

  // Handle search by applicant, street, or nearby
  const handleSearch = async () => {
    try {
      let results: FoodTruck[] = []
      switch (searchType) {
        case "applicant":
          results = await searchByApplicant(searchQuery, status)
          break
        case "street":
          results = await searchByStreet(searchQuery, status)
          break
        case "nearby":
          const latitude = parseFloat(lat)
          const longitude = parseFloat(lng)
          if (!isNaN(latitude) && !isNaN(longitude)) {
            results = await findNearbyTrucks(latitude, longitude, 5, status)
          }
          break
      }
      setData(results)
    } catch (error) {
      console.error("Error searching:", error)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="w-full max-w-screen-lg px-4">
        {/* Header */}
        <h1 className="text-3xl font-bold mb-8 text-center">🍔 SF Food Trucks</h1>

        {/* Search */}
        <div className="space-y-8">
          <div className="flex flex-col md:flex-row gap-4 items-stretch md:items-end">
            <div className="flex-1">
              <label className="text-sm font-medium mb-2 block">Search Type</label>
              <select
                className="w-full p-2 border rounded"
                value={searchType}
                onChange={(e) => setSearchType(e.target.value as "applicant" | "street" | "nearby")}
              >
                <option value="applicant">By Applicant</option>
                <option value="street">By Street</option>
                <option value="nearby">Nearby</option>
              </select>
            </div>

            {/* Search Query or Latitude */}
            <div className="flex-1">
              <label className="text-sm font-medium mb-2 block">
                {searchType === "nearby" ? "Latitude" : "Search Query"}
              </label>
              <input
                type={searchType === "nearby" ? "number" : "text"}
                className="w-full p-2 border rounded"
                value={searchType === "nearby" ? lat : searchQuery}
                onChange={(e) => {
                  if (searchType === "nearby") {
                    setLat(e.target.value)
                    setError("")
                  } else {
                    setSearchQuery(e.target.value)
                  }
                }}
                placeholder={
                  searchType === "applicant" 
                    ? "Enter applicant name" 
                    : searchType === "street"
                    ? "Enter street name"
                    : "e.g., 37.7749"
                }
              />
            </div>

            {/* Longitude (Nearby only) */}
            {searchType === "nearby" && (
              <div className="flex-1">
                <label className="text-sm font-medium mb-2 block">Longitude</label>
                <input
                  type="number"
                  className="w-full p-2 border rounded"
                  value={lng}
                  onChange={(e) => setLng(e.target.value)}
                  placeholder="e.g., -122.4194"
                />
              </div>
            )}

            {/* Status */}
            <div className="flex-1">
              <label className="text-sm font-medium mb-2 block">Status</label>
              <select
                className="w-full p-2 border rounded"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
              >
                <option value="APPROVED">Approved</option>
                <option value="REQUESTED">Requested</option>
                <option value="EXPIRED">Expired</option>
                <option value="SUSPEND">Suspended</option>
                <option value="ISSUED">Issued</option>
                <option value="">All Statuses</option>
              </select>
            </div>

            {/* Search Button */}
            <button
              className="w-full md:w-auto px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              onClick={handleSearch}
            >
              Search
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="text-red-500 text-sm mt-2 text-center">
              {error}
            </div>
          )}

          {/* Table with horizontal scroll */}
          <div className="overflow-x-auto rounded-lg">
            <DataTable columns={columns} data={data} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
