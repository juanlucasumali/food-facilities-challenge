import { FoodTruck } from "@/components/food-trucks/data-table"

const API_BASE_URL = "http://localhost:8000"

// Default headers for API requests
const defaultHeaders = {
  "Content-Type": "application/json",
  "Accept": "application/json",
}

async function fetchWithErrorHandling(url: string, options: RequestInit = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
      credentials: "include",
      mode: "cors", // Explicitly set CORS mode
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    return response.json()
  } catch (error) {
    console.error("API request failed:", error)
    throw error
  }
}

export async function searchByApplicant(query: string, status?: string): Promise<FoodTruck[]> {
  const params = new URLSearchParams({ q: query })
  if (status) params.append("status", status)
  
  return fetchWithErrorHandling(`${API_BASE_URL}/trucks/by-applicant?${params}`)
}

export async function searchByStreet(street: string, status?: string): Promise<FoodTruck[]> {
  const params = new URLSearchParams({ street })
  if (status) params.append("status", status)
  
  return fetchWithErrorHandling(`${API_BASE_URL}/trucks/by-street?${params}`)
}

export async function findNearbyTrucks(
  lat: number,
  lng: number,
  n: number = 5,
  status?: string
): Promise<FoodTruck[]> {
  const params = new URLSearchParams({
    lat: lat.toString(),
    lng: lng.toString(),
    n: n.toString()
  })
  if (status) params.append("status", status)
  
  return fetchWithErrorHandling(`${API_BASE_URL}/trucks/nearby?${params}`)
} 