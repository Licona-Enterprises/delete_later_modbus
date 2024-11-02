use modbus::{Client, tcp::Transport};
// use modbus::{Client, serial::SerialTransport};
// use tokio_serial::{SerialPortBuilder};
// use tokio_serial::SerialPortBuilderExt;
use tokio_serial::SerialStream;
use tokio::time::Duration;

// #[tokio::main]
async fn not_main() -> Result<(), Box<dyn std::error::Error>> {
    let tty_path = "/dev/ttyUSB0"; // Specify your device path

    // Open the serial port with a specified baud rate
    let port = tokio_serial::new(tty_path, 9600).open_native()?;
    // let mut port = tokio_serial::new(tty_path, 9600).open_native_async()?;
    // let port = tokio_serial::new(tty_path, 9600).open_native_async()?;

    // Create the Modbus TCP transport with the serial port
    let mut ctx = Transport::new(port)?;
    // let mut ctx = SerialTransport::new(port);
    // let mut ctx = Transport::new(port);

    // Send commands to the Modbus device
    // ctx.write_single_register(0x2000, 0x0001);
    // ctx.write_single_register(0x2001, 0x0032);
    // ctx.write_single_register(0x2002, 100);

    Ok(())
}
