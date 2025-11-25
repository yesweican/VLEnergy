namespace VXWebApp.Models
{
    public class RawData
    {
        public int ID { get; set; }
        public string Client_ID { get; set; }
        public string Device_ID { get; set; }
        public double Device_Reading { get; set; }
        public string Reading_Unit { get; set; }
        public DateTime TimeStamp { get; set; }
    }
}
