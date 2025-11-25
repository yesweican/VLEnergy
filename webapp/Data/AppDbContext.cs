using Microsoft.EntityFrameworkCore;
using VXWebApp.Models;

namespace VXWebApp.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options)
        {
        }

        public DbSet<RawData> Raw_Data { get; set; }
    }
}
