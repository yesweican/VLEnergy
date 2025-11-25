using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using VXWebApp.Data;

namespace VXWebApp.Controllers
{
    public class HomeController : Controller
    {
        private readonly AppDbContext _context;

        public HomeController(AppDbContext context)
        {
            _context = context;
        }

        public async Task<IActionResult> Index()
        {
            var data = await _context.Raw_Data
                .OrderByDescending(r => r.TimeStamp)
                .Take(100)
                .ToListAsync();

            return View(data);
        }
    }
}
