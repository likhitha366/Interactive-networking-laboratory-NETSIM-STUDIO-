import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/** Dependency-free local web server for NetSim Studio. */
public class NetSimServer {
    private static final Path ROOT = Paths.get("").toAbsolutePath();
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 5000), 0);
        server.createContext("/", NetSimServer::serve);
        server.setExecutor(null);
        server.start();
        System.out.println("NetSim Studio is running at http://127.0.0.1:5000");
        System.out.println("Press Ctrl+C to stop the server.");
    }
    private static void serve(HttpExchange exchange) throws IOException {
        if (!exchange.getRequestMethod().equals("GET")) { send(exchange, 405, "text/plain", "Method not allowed"); return; }
        String request = exchange.getRequestURI().getPath();
        if (request.equals("/")) request = "/templates/index.html";
        Path file = ROOT.resolve(request.substring(1)).normalize();
        if (!file.startsWith(ROOT) || !Files.isRegularFile(file)) { send(exchange, 404, "text/plain", "Page not found"); return; }
        String type = request.endsWith(".css") ? "text/css; charset=utf-8" : request.endsWith(".js") ? "application/javascript; charset=utf-8" : "text/html; charset=utf-8";
        byte[] body = Files.readAllBytes(file);
        exchange.getResponseHeaders().set("Content-Type", type);
        exchange.sendResponseHeaders(200, body.length);
        exchange.getResponseBody().write(body); exchange.close();
    }
    private static void send(HttpExchange e, int status, String type, String text) throws IOException {
        byte[] body = text.getBytes("UTF-8"); e.getResponseHeaders().set("Content-Type", type);
        e.sendResponseHeaders(status, body.length); e.getResponseBody().write(body); e.close();
    }
}
