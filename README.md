# 🍔 SF Food Trucks

<img width="1037" alt="Screenshot 2025-05-03 at 11 50 27 AM" src="https://github.com/user-attachments/assets/dfd02fdf-8bd4-4daf-b155-7acd7eeacd76" />

## 📜 How to run and test the app

1. **Create and Activate Python Virtual Environment**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install Python Dependencies**

    ```bash
    pip3 install -r requirements.txt
    ```

3. **Install Node.js Dependencies**

    ```bash
    npm install
    ```

4. **Start Docker**

    Make sure Docker Desktop is running.

5. **Set Up Environment Variables**

    Create a `.env` file in the root directory with the following content:

    ```
    DATABASE_URL=postgresql+asyncpg://foodtruck:foodtruck@localhost:5432/foodtruck
    ```

6. **Start the Application**

    ```bash
    make run
    ```

    Wait until you see: `database system is ready to accept connections`.

7. **Initialize the Database**

    Open a new terminal window, activate the environment again:

    ```bash
    source .venv/bin/activate
    make init-db
    ```

    - If you encounter:

        ```
        asyncpg.exceptions.InvalidAuthorizationSpecificationError: role "foodtruck" does not exist
        ```

        Run:

        ```bash
        brew services stop postgresql
        ```

        This stops any conflicting local Postgres service.

8. **(Optional) Access API Documentation**

    You can now visit the interactive FastAPI Swagger UI at:

    [http://localhost:8000/docs](http://localhost:8000/docs)

9. **Run Tests**

    ```bash
    make test
    ```

10. **Start Frontend Development Server**

    ```bash
    npm run dev
    ```

---

## ❓ The Challenge

The challenge was to use [this data set](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat/about_data) about Mobile Food Facilities in SF in order to build an app with the following features:

1. **Search by applicant name** (optionally filter by permit status)  
2. **Search by street name** with partial string matching (e.g. `"SAN"` → `SANSOME ST`)  
3. **Find the 5 trucks nearest a lat/lng** – default to *APPROVED* only, but allow override  
4. Provide **automated tests.**  
5. **Bonus features:** API documentation, a dockerfile, and a UI.

---

## ❗ The Solution

I wanted to create an app that was small yet mighty; something that mirrored a modern production stack:

| **Layer** | **Tech Choice** |
| --- | --- |
| `Database` | **PostgreSQL with PostGIS:** Geospatial capabilities via PostGIS (nearest trucks search)<br>**geoalchemy2:** Store location data as PostGIS POINT type (nearest trucks search) |
| `Backend` | **FastAPI:** Async web framework with API documentation and validation<br>**uvicorn:** ASGI server for FastAPI<br>**python-dotenv:** Env variable management |
| `ORM` | **SQLAlchemy:** Async support and type safety<br>**asyncpg:** Async PostgreSQL driver |
| `Frontend` | **React:** Component-based UI<br>**TypeScript:** Static typing<br>**Vite:** Fast build tool |
| `UI Components` | **shadcn/ui:** Customizable UI components built on Radix UI<br>**Tailwind CSS:** Utility-first styling |
| `Testing` | **pytest:** Python testing framework<br>**pytest-asyncio:** Async support<br>**httpx:** Async HTTP client for API testing |

---

## ⚒️ API Design

<img width="1322" alt="Screenshot 2025-05-03 at 11 48 21 AM" src="https://github.com/user-attachments/assets/c89cf4f9-487c-4e6e-b855-7a3ad28babc8" />


I made three endpoints that cover the spec. All parameters are type-checked by FastAPI. You can also visit an interactive API documentation rendered in FastAPI’s Swagger UI after you run the app:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

| Route | Example |
| --- | --- |
| `/trucks/by-applicant?q=TACO&status=` | Partial applicant match on `TACO`, trucks with any status |
| `/trucks/by-street?street=SAN&status=APPROVED` | Partial street match on `SAN`, only `APPROVED` trucks  |
| `/trucks/nearby?lat=37.79&lng=-122.40&n=5` | 5 closest trucks to specified latitude and longitude |

---

## 🧐 Critique

1. **What would you have done differently if you had spent more time on this?**
    
    I definitely learned a lot from this project! Did my fair share of using what I’ve learned/what I’m comfortable with while also dipping my toes into new technologies. However, there’s always room to improve:
    
    1. My automated tests could have been more comprehensive. I could’ve implemented more tests for database operations, frontend components, and query speed/performance. 
    2. I also could’ve spent more time on making more robust error handling, e.g. better error messages on the frontend and request validation. 
    3. Lastly, I tested the setup process on my housemate’s computers, and I was able to catch a few environment-related errors and find workarounds to them, but if I had more time I’d keep testing to find more potential bugs.
2. What are the trade-offs you might have made?
    1. I chose PostgreSQL over other simpler databases like SQLite because of its extensions. PostGIS’ geospatial queries was perfect for finding nearby food trucks, and pg_trgm was good for fuzzy matching. The downsides? A more complex setup, and pretty overkill for small datasets.
    2. I chose to to write my tests against the real production database instead of writing tests creating an identical mock database for each test run. There are a few cons for using the real database in testing, such as the potential to corrupt production data and the inability to isolate tests, but I found that it was a much simpler setup and still a viable method for this specific use-case. But if I had more time I’d definitely try out the mock database approach.
3. What are the things you left out?
    
    Some things that were left out due to the time crunch were the frontend component tests, robust error-handling, loading/error states in the frontend, and authentication.
    
4. What are the problems with your implementation and how would you solve them if we had to scale the application to a large number of users?
    1. The first thing that came to mind was that the app isn’t deployed and hosted on the cloud, so if we had to scale the app to a large number of users I’d probably host it on AWS or GCP so that people could use it anywhere anytime.
    2. Security and authentication is the second thing that came to my mind. I'd want to modify my FastAPI implementation to include rate limits and utilize an auth library (e.g. Supabase or NextAuth) to apply RLS in Postgres. These would ideally lower cloud costs and prevent malicious scripts from modifying the database.
    3. Next thing is implementing GitHub Actions to make the development and deployment pipeline easier. In case our users run into errors and bugs, we can fix and deploy them ASAP.
