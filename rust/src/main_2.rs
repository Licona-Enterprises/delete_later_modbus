use modbus::{Client, tcp::Transport};
use tokio_serial::SerialStream;
use tokio_serial::SerialPortBuilderExt;
use tokio_serial::new;
use tokio::time::Duration;

// #[tokio::main]
async fn not_main() -> Result<(), Box<dyn std::error::Error>> {
    let tty_path = "/dev/ttyUSB0"; // Specify your device path

    // --- for test delete here: 
    // Open the serial port with a specified baud rate
    // let port = new(tty_path, 9600).open_native_async()?;

    // // Now you can create your Modbus client
    // let mut ctx = Transport::new(tty_path);
    // --- end of test delete section


    // not async
    let port = tokio_serial::new(tty_path, 9600).open_native()?;
    let mut ctx = Transport::new(port)?;


    // async
    // let port = tokio_serial::new(tty_path, 9600).open_native_async()?;
    // let mut ctx = Transport::new(tty_path);

    // Send commands to the Modbus device
    ctx.write_single_register(0x2000, 0x0001).await?;
    ctx.write_single_register(0x2001, 0x0032).await?;
    ctx.write_single_register(0x2002, 100).await?;

    Ok(())
}
